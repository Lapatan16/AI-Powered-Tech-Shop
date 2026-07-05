import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import status
from src.api import api
from src.recommendations.recommendations_dependencies import get_rec_service
from src.auth.auth_dependencies import get_current_user
from src.recommendations.recommendations_service import RecommendationsService
from src.recommendations.recommendations_repository import RecommendationsRepository
from src.recommendations.recommendations_models import AiProductPredictionResponse
from src.products.products_models import ProductsPreviewModel
from src.users.users_models import UserResponseModel
from src.entities.recommendation_entity import RecommendationEntity
from src.entities.product_entity import ProductEntity

# setup

@pytest.fixture
def mock_rec_service():
    service = MagicMock(spec=RecommendationsService)
    service.get_personalized_recommendations_async = AsyncMock()
    service.autocomplete_product_fields_async = AsyncMock()
    return service

@pytest.fixture
def override_dependencies(mock_rec_service):
    mock_user = MagicMock(spec=UserResponseModel)
    mock_user.id = 1
    api.dependency_overrides[get_rec_service] = lambda: mock_rec_service
    api.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    api.dependency_overrides.clear()

@pytest.fixture
def mock_uow():
    uow_mock = MagicMock()
    uow_mock.recommendations = MagicMock()
    uow_mock.recommendations.get_recommended_products_by_user_id_async = AsyncMock()
    uow_mock.products = MagicMock()
    uow_mock.products.find_all_products_async = AsyncMock()
    uow_mock.products.find_product_categories_and_subcategories_async = AsyncMock()
    return uow_mock


# controller

@pytest.mark.asyncio
async def test_get_for_you_recommendations_router_success(client, mock_rec_service, override_dependencies):
    mock_preview = MagicMock(spec=ProductsPreviewModel)
    mock_preview.id = 10
    mock_preview.name = "Controller Product"
    mock_rec_service.get_personalized_recommendations_async.return_value = [mock_preview]
    
    response = client.get("/recommendations/for-you")
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_autocomplete_product_fields_router_success(client, mock_rec_service, override_dependencies):
    mock_prediction = MagicMock(spec=AiProductPredictionResponse)
    mock_prediction.name = "AI Product"
    mock_prediction.price = "45.50"
    mock_prediction.sub_category_id = 3
    mock_rec_service.autocomplete_product_fields_async.return_value = mock_prediction
    
    payload = {"user_prompt": "Mechanical gaming mouse"}
    response = client.post("/recommendations/autofill", json=payload)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "AI Product"

@pytest.mark.asyncio
async def test_autocomplete_product_fields_router_validation_error(client, mock_rec_service, override_dependencies):
    mock_rec_service.autocomplete_product_fields_async.side_effect = ValueError("Parsing failed")
    
    payload = {"user_prompt": "Invalid input"}
    response = client.post("/recommendations/autofill", json=payload)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert "Parsing failed" in response.json()["detail"]


# service

@pytest.mark.asyncio
async def test_service_get_personalized_recommendations_has_data(mock_uow):
    mock_image = MagicMock()
    mock_image.src = "keyboard.png"
    
    mock_product = MagicMock()
    mock_product.id = 15
    mock_product.name = "Custom Rec"
    mock_product.sub_category_id = 1
    mock_product.user_id = 1
    mock_product.price = "99.99"
    mock_product.stock = 10
    mock_product.discount = 0.0
    mock_product.images = [mock_image]
    mock_uow.recommendations.get_recommended_products_by_user_id_async.return_value = [mock_product]
    
    service = RecommendationsService(uow=mock_uow)
    result = await service.get_personalized_recommendations_async(user_id=1)
    
    assert len(result) == 1
    mock_uow.products.find_all_products_async.assert_not_called()

@pytest.mark.asyncio
async def test_service_get_personalized_recommendations_fallback(mock_uow):
    mock_uow.recommendations.get_recommended_products_by_user_id_async.return_value = []
    
    mock_image = MagicMock()
    mock_image.src = "fallback.png"
    
    mock_product = MagicMock()
    mock_product.id = 20
    mock_product.name = "Fallback Rec"
    mock_product.sub_category_id = 1
    mock_product.user_id = 1
    mock_product.price = "49.99"
    mock_product.stock = 5
    mock_product.discount = 0.0
    mock_product.images = [mock_image]
    mock_uow.products.find_all_products_async.return_value = ([mock_product], 1)
    
    service = RecommendationsService(uow=mock_uow)
    result = await service.get_personalized_recommendations_async(user_id=1)
    
    assert len(result) == 1
    mock_uow.products.find_all_products_async.assert_called_once()


# repository

@pytest.mark.asyncio
async def test_repository_get_recommended_products_empty():
    mock_db_context = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_db_context.execute = AsyncMock(return_value=mock_result)
    
    repo = RecommendationsRepository(db_context=mock_db_context)
    result = await repo.get_recommended_products_by_user_id_async(user_id=1)
    
    assert result == []

@pytest.mark.asyncio
async def test_repository_get_default_top_products_calls_db():
    mock_db_context = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = []
    mock_db_context.execute = AsyncMock(return_value=mock_result)
    
    repo = RecommendationsRepository(db_context=mock_db_context)
    result = await repo.get_default_top_products_async(limit=5)
    
    assert isinstance(result, list)
    assert mock_db_context.execute.call_count == 1