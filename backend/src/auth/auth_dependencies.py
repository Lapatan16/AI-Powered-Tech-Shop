from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from typing import Any

from .auth_repository import AuthRepository
from .auth_service import AuthService
from .jwt_helper import decode_access_token

from ..database.db import get_db
from ..users.users_dependencies import get_users_service
from ..users.users_service import UsersService
from ..users.users_models import UserResponseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_auth_repo(db: AsyncSession = Depends(get_db)) -> AuthRepository:
    return AuthRepository(db)

def get_auth_service(
    repo: AuthRepository = Depends(get_auth_repo),
    users_service: UsersService = Depends(get_users_service)
) -> AuthService:
    return AuthService(repo, users_service)

async def get_current_user(
    users_service: UsersService = Depends(get_users_service),
    token: str = Depends(oauth2_scheme)
) -> UserResponseModel:
    try:
        payload: dict[str, Any] = decode_access_token(token)
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, {
                "error": "token is not valid."
            })
        
        user = await users_service.get_user_by_username(username)

        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, {
                "error": "token is not valid."
            })
        
        return user
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, {
            "error": "token is not valid."
        })