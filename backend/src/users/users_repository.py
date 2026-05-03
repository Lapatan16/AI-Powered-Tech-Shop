from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..entities.user_entity import UserEntity

class UsersRepository():

    def __init__(self, db_context: AsyncSession):
        self.__db_context = db_context

    async def find_all_users_async(self) -> list[UserEntity]:
        statement = select(UserEntity)
        result = await self.__db_context.execute(statement)

        return result.scalars().all()
    
    async def find_user_by_username(self, username: str) -> UserEntity | None:
        statement = select(UserEntity).where(UserEntity.user_name == username)

        result = await self.__db_context.execute(statement)

        return result.scalar_one_or_none()
    
    async def find_user_by_email(self, email: str) -> UserEntity | None:
        statement = select(UserEntity).where(UserEntity.email == email)

        result = await self.__db_context.execute(statement)

        return result.scalar_one_or_none()