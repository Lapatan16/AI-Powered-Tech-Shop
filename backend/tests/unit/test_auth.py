import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import status
from src.api import api
from src.auth.auth_dependencies import get_auth_service
from src.auth.auth_exceptions import (
    UserNameAlreadyExistsError,
    EmailAlreadyExistsError,
    CredentialsDontMatchError
)
from src.carts.carts_exceptions import CartCreateError
from src.users.users_exceptions import NotFoundError
from src.auth.auth_service import AuthService
from src.auth.auth_repository import AuthRepository

# setup

@pytest.fixture
def mock_auth_service():
    """Creates an AsyncMock version of the AuthService business layer."""
    service = MagicMock(spec=AuthService)
    service.register_user_async = AsyncMock()
    service.login_user_async = AsyncMock()
    return service

@pytest.fixture
def override_dependencies(mock_auth_service):
    """Overwrites the FastAPI dependency tree to inject our mock service."""
    api.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    yield
    api.dependency_overrides.clear()

@pytest.fixture
def mock_uow(mocker):
    """Mocks the Unit of Work specifically inside the auth_service execution context."""
    uow_mock = MagicMock()
    uow_mock.users = MagicMock()
    uow_mock.users.find_user_by_username = AsyncMock()
    uow_mock.users.find_user_by_email = AsyncMock()
    uow_mock.auth = MagicMock()
    uow_mock.auth.save_user_async = AsyncMock()
    uow_mock.auth.find_user_for_login = AsyncMock()
    uow_mock.carts = MagicMock()
    uow_mock.carts.create_cart_async = AsyncMock()
    return uow_mock


# controller

@pytest.mark.asyncio
async def test_register_router_success(client, mock_auth_service, override_dependencies):
    mock_auth_service.register_user_async.return_value = "mocked_jwt_token_123"
    
    payload = {"user_name": "test_user", "email": "test@test.com", "password": "password123"}
    response = client.post("/auth/register", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["access_token"] == "mocked_jwt_token_123"

@pytest.mark.asyncio
async def test_register_router_username_taken(client, mock_auth_service, override_dependencies):
    mock_auth_service.register_user_async.side_effect = UserNameAlreadyExistsError()
    
    payload = {"user_name": "taken_user", "email": "test@test.com", "password": "password123"}
    response = client.post("/auth/register", json=payload)
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == {"error": "user_name is already taken."}

@pytest.mark.asyncio
async def test_login_router_invalid_credentials(client, mock_auth_service, override_dependencies):
    mock_auth_service.login_user_async.side_effect = CredentialsDontMatchError()
    
    form_data = {"username": "wrong_user", "password": "bad_password"}
    response = client.post("/auth/login", data=form_data)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == {"error": "credentials don't match."}


# service

@pytest.mark.asyncio
async def test_service_registration_duplicate_email_throws(mock_uow):
    mock_uow.users.find_user_by_username.side_effect = NotFoundError()
    mock_uow.users.find_user_by_email.return_value = MagicMock()  # Target email found
    
    service = AuthService(uow=mock_uow)
    user_data = MagicMock(user_name="new_user", email="taken@test.com", password="password")
    
    with pytest.raises(EmailAlreadyExistsError):
        await service.register_user_async(user_data)

@pytest.mark.asyncio
async def test_service_registration_cart_failure_throws(mock_uow):
    mock_uow.users.find_user_by_username.side_effect = NotFoundError()
    mock_uow.users.find_user_by_email.side_effect = NotFoundError()
    mock_uow.auth.save_user_async.return_value = MagicMock(id=1, user_name="user")
    mock_uow.carts.create_cart_async.return_value = None  # Simulating a failed cart creation
    
    service = AuthService(uow=mock_uow)
    user_data = MagicMock(user_name="new_user", email="test@test.com", password="password")
    
    with pytest.raises(CartCreateError):
        await service.register_user_async(user_data)


# repository

@pytest.mark.asyncio
async def test_repository_save_user_calls_db_context():
    mock_db_context = MagicMock()
    mock_db_context.add = MagicMock()
    mock_db_context.flush = AsyncMock()
    mock_db_context.refresh = AsyncMock()
    
    repo = AuthRepository(db_context=mock_db_context)
    user_data = MagicMock(user_name="db_user", email="db@test.com", password="hashed_password")
    
    await repo.save_user_async(user_data)
    
    assert mock_db_context.add.call_count == 1
    assert mock_db_context.flush.call_count == 1
    assert mock_db_context.refresh.call_count == 1