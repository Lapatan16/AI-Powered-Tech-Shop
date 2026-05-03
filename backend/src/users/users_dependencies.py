from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from .users_repository import UsersRepository
from .users_service import UsersService
from ..database.db import get_db

def get_users_repository(db_context: AsyncSession = Depends(get_db)) -> UsersRepository:
    return UsersRepository(db_context)

def get_users_service(repo: UsersRepository = Depends(get_users_repository)) -> UsersService:
    return UsersService(repo)