import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import api
from src.products.products_dependencies import get_products_service
from src.auth.auth_dependencies import get_current_user
from src.products.products_service import ProductsService
from src.products.products_repository import ProductsRepository
from src.products.products_models import ProductsUpdateModel
from src.products.products_query import ProductQueryParams
from src.entities.product_entity import ProductEntity
from src.entities.category_entity import CategoryEntity

# setup

@pytest.fixture
def mock_products_service():
    service = MagicMock(spec=ProductsService)
    service.get_all_products_async = AsyncMock()
    service.get_product_by_id_async = AsyncMock()
    service.create_product_async = AsyncMock()
    service.update_product_async = AsyncMock()
    service.delete_product_secure_async = AsyncMock()
    return service

@pytest.fixture
def override_dependencies(mock_products_service):
    mock_user = MagicMock(id=1)
    api.dependency_overrides[get_products_service] = lambda: mock_products_service
    api.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    api.dependency_overrides.clear()

@pytest.fixture
def mock_uow():
    uow_mock = MagicMock()
    uow_mock.products = MagicMock()
    uow_mock.products.find_all_products_async = AsyncMock()
    uow_mock.products.find_product_by_id_async = AsyncMock()
    uow_mock.products.create_product_async = AsyncMock()
    uow_mock.products.update_product_async = AsyncMock()
    uow_mock.products.delete_product_async = AsyncMock()
    return uow_mock


# controller

@pytest.mark.asyncio
async def test_get_all_products_success(client, mock_products_service, override_dependencies):
    mock_products_service.get_all_products_async.return_value = ([], 0)
    
    response = client.get("/products/all?page=1&limit=10")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert data["total_records"] == 0

@pytest.mark.asyncio
async def test_get_product_by_id_not_found(client, mock_products_service, override_dependencies):
    from src.products.products_exceptions import ProductNotFoundError
    mock_products_service.get_product_by_id_async.side_effect = ProductNotFoundError("Product not found")
    
    response = client.get("/products/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["error"] == "Product not found"

@pytest.mark.asyncio
async def test_create_product_success(client, mock_products_service, override_dependencies):
    mock_product = MagicMock()
    mock_product.id = 1
    mock_product.name = "Mechanical Keyboard"
    mock_products_service.create_product_async.return_value = mock_product
    
    form_data = {
        "name": "Mechanical Keyboard",
        "sub_category_id": "5",
        "description": "RGB Backlit",
        "price": "99.99",
        "stock": "10",
        "discount": "0.0"
    }
    files = [("images", ("keyboard.jpg", b"fake_bytes", "image/jpeg"))]
    
    response = client.post("/products/", data=form_data, files=files)

@pytest.mark.asyncio
async def test_update_product_forbidden(client, mock_products_service, override_dependencies):
    mock_products_service.update_product_async.side_effect = PermissionError("Not authorized to modify this product")
    
    payload = {
        "name": "Hacked Title",
        "description": "Exploit",
        "sub_category_id": 1,
        "price": 10.0,
        "stock": 1,
        "discount": 0.0
    }
    
    response = client.put("/products/42", json=payload)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Not authorized" in response.json()["detail"]["error"]


# service

@pytest.mark.asyncio
async def test_service_get_product_by_id_raises_not_found(mock_uow):
    from src.products.products_exceptions import ProductNotFoundError
    mock_uow.products.find_product_by_id_async.return_value = None
    
    service = ProductsService(uow=mock_uow)
    
    with pytest.raises(ProductNotFoundError):
        await service.get_product_by_id_async(100)

@pytest.mark.asyncio
async def test_service_update_product_ownership_violation(mock_uow):
    mock_product = MagicMock(spec=ProductEntity)
    mock_product.id = 10
    mock_product.user_id = 100
    mock_product.is_deleted = False
    mock_uow.products.find_product_by_id_async.return_value = mock_product
    
    service = ProductsService(uow=mock_uow)
    update_model = ProductsUpdateModel(
        name="Update", description="", sub_category_id=1, price=10.0, stock=5, discount=0.0
    )
    
    with pytest.raises(PermissionError, match="You do not own this product listing."):
        await service.update_product_async(product_id=10, user_id=999, model=update_model)

@pytest.mark.asyncio
async def test_service_delete_product_secure_success(mock_uow):
    mock_product = MagicMock(spec=ProductEntity)
    mock_product.id = 5
    mock_product.user_id = 200
    mock_product.is_deleted = False
    mock_uow.products.find_product_by_id_async.return_value = mock_product
    
    service = ProductsService(uow=mock_uow)
    await service.delete_product_secure_async(product_id=5, user_id=200)
    
    mock_uow.products.delete_product_async.assert_awaited_once_with(5)


# repository

@pytest.mark.asyncio
async def test_repository_find_all_products_filters_by_subcategory():
    mock_db_context = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalar_one.return_value = 0
    mock_result.scalars.return_value.all.return_value = []
    mock_db_context.execute = AsyncMock(return_value=mock_result)
    
    repo = ProductsRepository(db_context=mock_db_context)
    params = ProductQueryParams(sub_category_id=4, page=1, limit=10)
    
    await repo.find_all_products_async(params)
    
    assert mock_db_context.execute.call_count == 2
    executed_statements = [call[0][0] for call in mock_db_context.execute.call_args_list]
    assert any("sub_category_id = :" in str(stmt) for stmt in executed_statements)

@pytest.mark.asyncio
async def test_repository_create_product_flushes_and_links_images():
    mock_db_context = MagicMock(spec=AsyncSession)
    mock_db_context.add = MagicMock()
    mock_db_context.flush = AsyncMock()
    
    repo = ProductsRepository(db_context=mock_db_context)
    images = ["/static/uploads/img1.png", "/static/uploads/img2.png"]
    
    product = await repo.create_product_async(
        name="Test Item",
        description="Desc",
        sub_category_id=1,
        user_id=1,
        price=15.0,
        stock=10,
        discount=0.0,
        image_src_list=images
    )
    
    assert mock_db_context.add.call_count == 3
    assert mock_db_context.flush.call_count == 2
    assert product.name == "Test Item"