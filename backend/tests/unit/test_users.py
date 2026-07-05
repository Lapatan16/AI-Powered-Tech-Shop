import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import status
from src.api import api
from src.users.users_dependencies import get_users_service
from src.auth.auth_dependencies import get_current_user
from src.users.users_service import UsersService
from src.users.users_repository import UsersRepository
from src.users.users_models import UserResponseModel, DashboardAnalyticsResponse, SummaryMetrics, DashboardCharts
from src.users.users_exceptions import NotFoundError
from src.entities.user_entity import UserEntity

# setup

@pytest.fixture
def mock_users_service():
    service = MagicMock(spec=UsersService)
    service.get_all_users_async = AsyncMock()
    service.get_user_by_username = AsyncMock()
    service.get_user_by_email = AsyncMock()
    service.get_dashboard_analytics_by_user_id_async = AsyncMock()
    return service

@pytest.fixture
def override_dependencies(mock_users_service):
    mock_user = MagicMock(spec=UserResponseModel)
    mock_user.id = 1
    mock_user.user_name = "test_user"
    mock_user.email = "test@test.com"
    api.dependency_overrides[get_users_service] = lambda: mock_users_service
    api.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    api.dependency_overrides.clear()

@pytest.fixture
def mock_uow():
    uow_mock = MagicMock()
    uow_mock.users = MagicMock()
    uow_mock.users.find_all_users_async = AsyncMock()
    uow_mock.users.find_user_by_username = AsyncMock()
    uow_mock.users.find_user_by_email = AsyncMock()
    uow_mock.products = MagicMock()
    uow_mock.products.get_seller_summary_metrics_async = AsyncMock()
    uow_mock.products.get_seller_chart_analytics_async = AsyncMock()
    return uow_mock


# controller

@pytest.mark.asyncio
async def test_get_current_user_router_success(client, override_dependencies):
    response = client.get("/users/current_user")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_name"] == "test_user"

@pytest.mark.asyncio
async def test_get_seller_dashboard_analytics_router_success(client, mock_users_service, override_dependencies):
    mock_analytics = MagicMock(spec=DashboardAnalyticsResponse)
    mock_analytics.summary_metrics = MagicMock(spec=SummaryMetrics)
    mock_analytics.charts = MagicMock(spec=DashboardCharts)
    mock_users_service.get_dashboard_analytics_by_user_id_async.return_value = mock_analytics
    
    response = client.get("/users/dashboard/analytics")
    
    assert response.status_code == status.HTTP_200_OK


# service

@pytest.mark.asyncio
async def test_service_get_user_by_username_success(mock_uow):
    mock_user_entity = MagicMock(spec=UserEntity)
    mock_user_entity.id = 1
    mock_user_entity.user_name = "john_doe"
    mock_user_entity.email = "john@test.com"
    mock_uow.users.find_user_by_username.return_value = mock_user_entity
    
    service = UsersService(uow=mock_uow)
    result = await service.get_user_by_username("john_doe")
    
    assert result.user_name == "john_doe"

@pytest.mark.asyncio
async def test_service_get_user_by_username_throws_not_found(mock_uow):
    mock_uow.users.find_user_by_username.return_value = None
    
    service = UsersService(uow=mock_uow)
    
    with pytest.raises(NotFoundError):
        await service.get_user_by_username("missing_user")

@pytest.mark.asyncio
async def test_service_get_dashboard_analytics_success(mock_uow):
    mock_uow.products.get_seller_summary_metrics_async.return_value = {
        "total_revenue": 1500.0,
        "total_sales": 30,
        "units_sold": 45,
        "active_listings_count": 12,
        "out_of_stock_count": 2
    }
    mock_uow.products.get_seller_chart_analytics_async.return_value = {
        "revenue_trend": [
            {"date": "2026-01", "revenue": 500.0},
            {"date": "2026-02", "revenue": 1000.0}
        ],
        "category_distribution": [
            {"name": "Laptops", "value": 10},
            {"name": "Phones", "value": 20}
        ],
        "stock_vs_sales": [
            {"name": "Logitech G Pro", "sold": 30, "stock": 70},
            {"name": "ASUS ROG Strix", "sold": 15, "stock": 5}
        ]
    }
    
    service = UsersService(uow=mock_uow)
    result = await service.get_dashboard_analytics_by_user_id_async(user_id=1)
    
    assert isinstance(result, DashboardAnalyticsResponse)
    mock_uow.products.get_seller_summary_metrics_async.assert_called_once_with(1)
    mock_uow.products.get_seller_chart_analytics_async.assert_called_once_with(1)

# repository

@pytest.mark.asyncio
async def test_repository_find_user_by_username_calls_db():
    mock_db_context = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = MagicMock(spec=UserEntity)
    mock_db_context.execute = AsyncMock(return_value=mock_result)
    
    repo = UsersRepository(db_context=mock_db_context)
    await repo.find_user_by_username("db_user")
    
    assert mock_db_context.execute.call_count == 1

@pytest.mark.asyncio
async def test_repository_find_user_by_email_calls_db():
    mock_db_context = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_context.execute = AsyncMock(return_value=mock_result)
    
    repo = UsersRepository(db_context=mock_db_context)
    result = await repo.find_user_by_email("missing@test.com")
    
    assert result is None
    assert mock_db_context.execute.call_count == 1