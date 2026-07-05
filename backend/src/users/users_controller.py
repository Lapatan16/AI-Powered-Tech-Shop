from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated

from .users_models import DashboardAnalyticsResponse, UserResponseModel
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
    "/current_user",
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK
)
async def get_current_user_async(
    current_user: UserResponseModel = Depends(get_current_user)
) -> UserResponseModel:
    return current_user

@router.get(
    "/dashboard/analytics",
    response_model=DashboardAnalyticsResponse,
    status_code=status.HTTP_200_OK
)
async def get_seller_dashboard_analytics_async(
    users_service: usersServiceDependency,
    current_user: UserResponseModel = Depends(get_current_user)
) -> DashboardAnalyticsResponse:
    return await users_service.get_dashboard_analytics_by_user_id_async(current_user.id)