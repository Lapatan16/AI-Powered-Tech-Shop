import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from fastapi import status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.api import api
from src.orders.orders_dependencies import get_orders_service
from src.auth.auth_dependencies import get_current_user
from src.orders.orders_service import OrdersService
from src.orders.orders_repository import OrdersRepository
from src.orders.orders_models import OrderResponseModel
from src.entities.order_entity import OrderEntity
from src.entities.cart_entity import CartEntity

# setup

@pytest.fixture
def mock_orders_service():
    service = MagicMock(spec=OrdersService)
    service.checkout_cart_async = AsyncMock()
    return service

@pytest.fixture
def override_dependencies(mock_orders_service):
    mock_user = MagicMock(id=1)
    api.dependency_overrides[get_orders_service] = lambda: mock_orders_service
    api.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    api.dependency_overrides.clear()

@pytest.fixture
def mock_uow():
    uow_mock = MagicMock()
    uow_mock.carts = MagicMock()
    uow_mock.orders = MagicMock()
    uow_mock.carts.find_cart_with_products_by_user_id_async = AsyncMock()
    uow_mock.orders.create_order_from_cart_async = AsyncMock()
    uow_mock.commit = AsyncMock()
    return uow_mock


# controller

@pytest.mark.asyncio
async def test_checkout_success(client, mock_orders_service, override_dependencies):
    mock_orders_service.checkout_cart_async.return_value = {
        "order_id": 1,
        "total_price": 1500.0,
        "created_at": "2026-07-05T16:09:00",
        "items": []
    }
    
    response = client.post("/orders/checkout")
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["order_id"] == 1
    assert response.json()["total_price"] == 1500.0


# service

@pytest.mark.asyncio
async def test_service_checkout_empty_cart_throws(mock_uow):
    mock_uow.carts.find_cart_with_products_by_user_id_async.return_value = None
    bg_tasks = MagicMock(spec=BackgroundTasks)
    
    service = OrdersService(uow=mock_uow)
    
    with pytest.raises(ValueError, match="Cannot checkout an empty shopping cart configuration."):
        await service.checkout_cart_async(user_id=1, background_tasks=bg_tasks)

@pytest.mark.asyncio
async def test_service_checkout_deleted_product_throws(mock_uow):
    mock_product = MagicMock()
    mock_product.is_deleted = True
    mock_product.name = "Defunct Item"
    
    mock_item = MagicMock()
    mock_item.product = mock_product
    
    mock_bridge = MagicMock()
    mock_bridge.product_in_cart = mock_item
    
    mock_cart = MagicMock()
    mock_cart.product_cart = [mock_bridge]
    
    mock_uow.carts.find_cart_with_products_by_user_id_async.return_value = mock_cart
    bg_tasks = MagicMock(spec=BackgroundTasks)
    
    service = OrdersService(uow=mock_uow)
    
    with pytest.raises(ValueError, match="Product 'Defunct Item' is no longer available"):
        await service.checkout_cart_async(user_id=1, background_tasks=bg_tasks)

@pytest.mark.asyncio
async def test_service_checkout_insufficient_stock_throws(mock_uow):
    mock_product = MagicMock()
    mock_product.is_deleted = False
    mock_product.name = "GPU"
    mock_product.stock = 1
    
    mock_item = MagicMock()
    mock_item.product = mock_product
    mock_item.amount = 5
    
    mock_bridge = MagicMock()
    mock_bridge.product_in_cart = mock_item
    
    mock_cart = MagicMock()
    mock_cart.product_cart = [mock_bridge]
    
    mock_uow.carts.find_cart_with_products_by_user_id_async.return_value = mock_cart
    bg_tasks = MagicMock(spec=BackgroundTasks)
    
    service = OrdersService(uow=mock_uow)
    
    with pytest.raises(ValueError, match="Insufficient stock for 'GPU'"):
        await service.checkout_cart_async(user_id=1, background_tasks=bg_tasks)

@pytest.mark.asyncio
async def test_service_checkout_success(mock_uow):
    mock_product = MagicMock()
    mock_product.is_deleted = False
    mock_product.stock = 10
    
    mock_item = MagicMock()
    mock_item.product = mock_product
    mock_item.amount = 2
    
    mock_bridge = MagicMock()
    mock_bridge.product_in_cart = mock_item
    
    mock_cart = MagicMock()
    mock_cart.product_cart = [mock_bridge]
    
    mock_order_item = MagicMock()
    mock_order_item.product_name = "Laptop"
    mock_order_item.price_at_purchase = 1000.0
    mock_order_item.quantity = 2
    
    mock_order = MagicMock()
    mock_order.id = 100
    mock_order.total_price = 2000.0
    mock_order.created_at = datetime(2026, 7, 5, 16, 9, 0)
    mock_order.items = [mock_order_item]
    
    mock_uow.carts.find_cart_with_products_by_user_id_async.return_value = mock_cart
    mock_uow.orders.create_order_from_cart_async.return_value = mock_order
    
    bg_tasks = MagicMock(spec=BackgroundTasks)
    bg_tasks.add_task = MagicMock()
    
    service = OrdersService(uow=mock_uow)
    result = await service.checkout_cart_async(user_id=1, background_tasks=bg_tasks)
    
    assert isinstance(result, OrderResponseModel)
    assert result.order_id == 100
    assert result.total_price == 2000.0
    assert result.items[0].product_name == "Laptop"
    mock_uow.commit.assert_called_once()
    bg_tasks.add_task.assert_called_once()


# repository

@pytest.mark.asyncio
async def test_repository_create_order_calculates_price_and_discounts():
    mock_db_context = MagicMock(spec=AsyncSession)
    mock_db_context.add = MagicMock()
    mock_db_context.flush = AsyncMock()
    mock_db_context.delete = AsyncMock()
    
    mock_product = MagicMock()
    mock_product.id = 10
    mock_product.name = "Tablet"
    mock_product.stock = 5
    mock_product.price = 100.0
    mock_product.discount = 10.0
    
    mock_item_in_cart = MagicMock()
    mock_item_in_cart.amount = 2
    mock_item_in_cart.product = mock_product
    
    mock_bridge = MagicMock()
    mock_bridge.product_in_cart = mock_item_in_cart
    
    mock_cart = MagicMock(spec=CartEntity)
    mock_cart.product_cart = [mock_bridge]
    
    mock_fully_loaded_order = MagicMock(spec=OrderEntity)
    mock_result = MagicMock()
    mock_result.scalars().one.return_value = mock_fully_loaded_order
    mock_db_context.execute = AsyncMock(return_value=mock_result)
    
    repo = OrdersRepository(db_context=mock_db_context)
    result = await repo.create_order_from_cart_async(user_id=1, cart=mock_cart)
    
    assert mock_product.stock == 3
    assert result == mock_fully_loaded_order
    mock_db_context.flush.assert_called()
    mock_db_context.delete.assert_called()