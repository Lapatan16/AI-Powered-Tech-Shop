from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import Annotated

from .carts_models import (
    CartResponseModel,
    CartCreateModel,
    CartMinResponseModel,
    CartAddProductModel,
    CartUpdateModel
)
from .carts_service import CartsService
from .carts_dependencies import get_carts_service
from .carts_exceptions import CartNotFoundError, ProductAlreadyInCartError

from ..users.users_models import UserResponseModel
from ..auth.auth_dependencies import get_current_user

router = APIRouter(
    prefix='/carts',
    tags=["Carts"]
)

@router.post('/', response_model=CartMinResponseModel)
async def create_cart(
    cart: CartCreateModel,
    carts_service: Annotated[CartsService, Depends(get_carts_service)]
):
    try:
        newCart = await carts_service.create_cart_async(cart)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Failed to create cart."))
    
    return newCart

@router.delete('/{cart_id}')
async def delete_cart(
    cart_id: int,
    carts_service: Annotated[CartsService, Depends(get_carts_service)]
):
    try:
        await carts_service.delete_cart_async(cart_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Failed to delete cart with id {cart_id}."))
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/items', response_model=CartResponseModel)
async def get_cart_for_user(
    carts_service: Annotated[CartsService, Depends(get_carts_service)],
    current_user: UserResponseModel = Depends(get_current_user)
):
    try:
        cart = await carts_service.get_cart_by_user_id_async(current_user.id)
    except CartNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    return cart

@router.post('/add-product')
async def add_product_to_cart(
    data: CartAddProductModel,
    carts_service: Annotated[CartsService, Depends(get_carts_service)],
    current_user: UserResponseModel = Depends(get_current_user)
):
    try:
        await carts_service.add_product_to_cart_async(current_user.id, data)
    except CartNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductAlreadyInCartError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Failed to add product with id {data.product_id} to cart."))
    
    return Response(status_code=status.HTTP_201_CREATED)

@router.delete('/remove-product/{product_id}')
async def remove_product_from_cart(
    product_id: int,
    carts_service: Annotated[CartsService, Depends(get_carts_service)],
    current_user: UserResponseModel = Depends(get_current_user)
):
    await carts_service.remove_product_from_cart_async(current_user.id, product_id)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/update-product-quantity')
async def update_cart_quantity(
    data: CartUpdateModel,
    carts_service: Annotated[CartsService, Depends(get_carts_service)],
    current_user: UserResponseModel = Depends(get_current_user)
):
    try:
        response = await carts_service.update_cart_quantity_async(current_user.id, data.product_id, data.new_amount, data.increase)
    except CartNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Failed to update quantity for product with id {data.product_id} in cart."))
    
    return response