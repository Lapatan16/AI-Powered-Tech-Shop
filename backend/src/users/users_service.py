from .users_repository import UsersRepository
from .users_models import UserResponseModel
from .users_exceptions import *

class UsersService():
    
    def __init__(self, repo: UsersRepository):
        self.__repo = repo

    async def get_all_users_async(self) -> list[UserResponseModel]:
        result = await self.__repo.find_all_users_async()

        return [UserResponseModel.model_validate(user) for user in result]
    
    async def get_user_by_username(self, username: str) -> UserResponseModel | None:
        result = await self.__repo.find_user_by_username(username)

        if not result:
            raise NotFoundError(f"user with username: {username} not found.")

        return UserResponseModel.model_validate(result)
    
    async def get_user_by_email(self, email: str) -> UserResponseModel:
        result = await self.__repo.find_user_by_email(email)

        if not result:
            raise NotFoundError(f"user with email: {email} not found.")

        return UserResponseModel.model_validate(result)