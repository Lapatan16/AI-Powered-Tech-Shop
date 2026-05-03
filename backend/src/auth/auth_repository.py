from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..entities.user_entity import UserEntity
from ..users.users_models import UserCreateModel

class AuthRepository():

    def __init__(self, db_context: AsyncSession):
        self.__db_context = db_context

    async def save_user_async(self, user: UserCreateModel) -> UserEntity:
        new_user = UserEntity(
            user_name=user.user_name,
            email=user.email,
            password=user.password
        )

        self.__db_context.add(new_user)
        await self.__db_context.flush()
        await self.__db_context.refresh(new_user)

        return new_user
    
    async def find_user_for_login(self, user_name: str) -> UserEntity | None:
        statement = select(UserEntity).where(UserEntity.user_name == user_name)

        user_from_db = await self.__db_context.execute(statement)

        return user_from_db.scalar_one_or_none()