from fastapi import APIRouter, Depends, status, BackgroundTasks
from typing import Annotated

from .orders_service import OrdersService, OrderResponseModel

from ..orders.orders_dependencies import get_orders_service
from ..users.users_models import UserResponseModel
from ..auth.auth_dependencies import get_current_user

router = APIRouter(
    prefix='/orders',
    tags=["Orders"]
)

@router.post('/checkout', response_model=OrderResponseModel, status_code=status.HTTP_201_CREATED)
async def checkout(
    orders_service: Annotated[OrdersService, Depends(get_orders_service)],
    background_tasks: BackgroundTasks,
    current_user: UserResponseModel = Depends(get_current_user)
):
    result = await orders_service.checkout_cart_async(current_user.id, background_tasks)
    return result