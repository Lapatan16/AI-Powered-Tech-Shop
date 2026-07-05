import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api import api
from src.carts.carts_dependencies import get_carts_service
from src.auth.auth_dependencies import get_current_user
from src.carts.carts_exceptions import CartNotFoundError, ProductAlreadyInCartError
from src.carts.carts_service import CartsService
from src.carts.carts_repository import CartsRepository
from src.carts.carts_models import CartCreateModel, CartAddProductModel, CartResponseModel, CartUpdateResponseModel
from src.entities.cart_entity import CartEntity

# setup

@pytest.fixture
def mock_carts_service():
    service = MagicMock(spec=CartsService)
    service.get_cart_by_user_id_async = AsyncMock()
    service.add_product_to_cart_async = AsyncMock()
    service.remove_product_from_cart_async = AsyncMock()
    service.update_cart_quantity_async = AsyncMock()
    return service

@pytest.fixture
def override_dependencies(mock_carts_service):
    mock_user = MagicMock(id=1)
    api.dependency_overrides[get_carts_service] = lambda: mock_carts_service
    api.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    api.dependency_overrides.clear()

@pytest.fixture
def mock_uow(mocker):
    uow_mock = MagicMock()
    uow_mock.carts = MagicMock()
    uow_mock.carts.create_cart_async = AsyncMock()
    uow_mock.carts.delete_cart_async = AsyncMock()
    uow_mock.carts.find_cart_with_products_by_user_id_async = AsyncMock()
    uow_mock.carts.find_cart_by_user_id_async = AsyncMock()
    uow_mock.carts.find_product_in_cart_async = AsyncMock()
    uow_mock.carts.save_product_in_cart_async = AsyncMock()
    uow_mock.carts.save_product_cart_async = AsyncMock()
    uow_mock.carts.delete_product_from_cart_async = AsyncMock()
    uow_mock.carts.update_cart_quantity_async = AsyncMock()
    return uow_mock


# controller

@pytest.mark.asyncio
async def test_get_cart_for_user_success(client, mock_carts_service, override_dependencies):
    mock_carts_service.get_cart_by_user_id_async.return_value = {"cart_id": 1, "user_id": 1, "items": []}
    
    response = client.get("/carts/items")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["cart_id"] == 1

@pytest.mark.asyncio
async def test_get_cart_for_user_not_found(client, mock_carts_service, override_dependencies):
    mock_carts_service.get_cart_by_user_id_async.side_effect = CartNotFoundError("Not found")
    
    response = client.get("/carts/items")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_add_product_to_cart_success(client, mock_carts_service, override_dependencies):
    mock_carts_service.add_product_to_cart_async.return_value = None
    
    payload = {"product_id": 42, "amount": 2}
    response = client.post("/carts/add-product", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_add_product_to_cart_already_exists(client, mock_carts_service, override_dependencies):
    mock_carts_service.add_product_to_cart_async.side_effect = ProductAlreadyInCartError("Already inside")
    
    payload = {"product_id": 42, "amount": 2}
    response = client.post("/carts/add-product", json=payload)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_remove_product_from_cart_success(client, mock_carts_service, override_dependencies):
    mock_carts_service.remove_product_from_cart_async.return_value = None
    
    response = client.delete("/carts/remove-product/42")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio
async def test_update_cart_quantity_success(client, mock_carts_service, override_dependencies):
    mock_carts_service.update_cart_quantity_async.return_value = {"product_id": 42, "new_amount": 5}
    
    payload = {"product_id": 42, "new_amount": 5, "increase": False}
    response = client.put("/carts/update-product-quantity", json=payload)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["new_amount"] == 5


# service

@pytest.mark.asyncio
async def test_service_get_cart_not_found_throws(mock_uow):
    mock_uow.carts.find_cart_with_products_by_user_id_async.return_value = None
    
    service = CartsService(uow=mock_uow)
    
    with pytest.raises(CartNotFoundError):
        await service.get_cart_by_user_id_async(user_id=1)

@pytest.mark.asyncio
async def test_service_get_cart_success_with_items(mock_uow):
    mock_image = MagicMock()
    mock_image.src = "image.png"
    
    mock_product = MagicMock()
    mock_product.id = 10
    mock_product.name = "Phone"
    mock_product.price = 500.0
    mock_product.images = [mock_image]
    
    mock_item_in_cart = MagicMock()
    mock_item_in_cart.id = 5
    mock_item_in_cart.amount = 2
    mock_item_in_cart.product = mock_product
    
    mock_bridge = MagicMock()
    mock_bridge.product_in_cart = mock_item_in_cart
    
    mock_cart = MagicMock()
    mock_cart.id = 1
    mock_cart.user_id = 1
    mock_cart.product_cart = [mock_bridge]
    
    mock_uow.carts.find_cart_with_products_by_user_id_async.return_value = mock_cart
    
    service = CartsService(uow=mock_uow)
    result = await service.get_cart_by_user_id_async(user_id=1)
    
    assert isinstance(result, CartResponseModel)
    assert result.cart_id == 1
    assert result.items[0].name == "Phone"
    assert result.items[0].image == "image.png"

@pytest.mark.asyncio
async def test_service_add_product_already_in_cart_throws(mock_uow):
    mock_uow.carts.find_product_in_cart_async.return_value = MagicMock()
    
    service = CartsService(uow=mock_uow)
    data = CartAddProductModel(product_id=42, amount=1)
    
    with pytest.raises(ProductAlreadyInCartError):
        await service.add_product_to_cart_async(user_id=1, data=data)

@pytest.mark.asyncio
async def test_service_add_product_cart_not_found_throws(mock_uow):
    mock_uow.carts.find_product_in_cart_async.return_value = None
    mock_uow.carts.find_cart_by_user_id_async.return_value = None
    
    service = CartsService(uow=mock_uow)
    data = CartAddProductModel(product_id=42, amount=1)
    
    with pytest.raises(CartNotFoundError):
        await service.add_product_to_cart_async(user_id=1, data=data)

@pytest.mark.asyncio
async def test_service_update_quantity_decrease_to_zero_deletes(mock_uow):
    service = CartsService(uow=mock_uow)
    
    result = await service.update_cart_quantity_async(user_id=1, product_id=42, new_amount=0, increase=False)
    
    mock_uow.carts.delete_product_from_cart_async.assert_called_once_with(1, 42)
    assert result.new_amount == 0


# repository

@pytest.mark.asyncio
async def test_repository_create_cart_flushes_db():
    mock_db_context = MagicMock(spec=AsyncSession)
    mock_db_context.add = MagicMock()
    mock_db_context.flush = AsyncMock()
    
    repo = CartsRepository(db_context=mock_db_context)
    model = CartCreateModel(user_id=1)
    
    result = await repo.create_cart_async(model)
    
    assert isinstance(result, CartEntity)
    mock_db_context.add.assert_called_once()
    mock_db_context.flush.assert_called_once()

@pytest.mark.asyncio
async def test_repository_delete_cart_executes_when_found():
    mock_db_context = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_cart = MagicMock()
    mock_result.scalars().first.return_value = mock_cart
    mock_db_context.execute = AsyncMock(return_value=mock_result)
    mock_db_context.delete = AsyncMock()
    
    repo = CartsRepository(db_context=mock_db_context)
    await repo.delete_cart_async(cart_id=1)
    
    mock_db_context.delete.assert_called_once_with(mock_cart)