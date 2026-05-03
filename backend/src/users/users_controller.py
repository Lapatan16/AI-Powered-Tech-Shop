from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated

from .users_models import UserResponseModel
from .users_service import UsersService
from .users_dependencies import get_users_service
from .users_exceptions import *
from ..auth.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

usersServiceDependency = Annotated[UsersService, Depends(get_users_service)]

@router.get(
    "/",
    response_model=list[UserResponseModel],
    status_code=status.HTTP_200_OK
)
async def get_all_users_async(
    users_service: usersServiceDependency
) -> list[UserResponseModel]:
    return await users_service.get_all_users_async()

@router.get(
    '/user_name/{user_name}',
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK
)
async def get_user_by_username(
    user_name: str,
    users_service: usersServiceDependency
) -> UserResponseModel:
    try:
        return await users_service.get_user_by_username(user_name)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={
            "error": str(e)
        })

@router.get(
    '/email/{email}',
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK
)
async def get_user_by_email(
    email: str,
    users_service: usersServiceDependency
) -> UserResponseModel:
    try:
        return await users_service.get_user_by_email(email)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={
            "error": str(e)
        })
    
@router.get(
    "/current_user",
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK
)
async def get_current_user_async(
    current_user: UserResponseModel = Depends(get_current_user)
) -> UserResponseModel:
    return current_user