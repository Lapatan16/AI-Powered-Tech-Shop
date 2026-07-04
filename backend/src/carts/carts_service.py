from .carts_models import (
    CartResponseModel,
    CartCreateModel,
    CartMinResponseModel,
    CartItemResponseModel,
    CartAddProductModel,
    CartUpdateResponseModel
)
from .carts_exceptions import CartNotFoundError, ProductAlreadyInCartError

from ..database.unit_of_work import UnitOfWork

class CartsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_cart_async(self, cart_create_model: CartCreateModel) -> CartMinResponseModel:
        newCart = await self.uow.carts.create_cart_async(cart_create_model)
        
        return CartMinResponseModel(
            id=newCart.id,
            user_id=newCart.user_id
        )
    
    async def delete_cart_async(self, cart_id: int):
        await self.uow.carts.delete_cart_async(cart_id)

    async def get_cart_by_user_id_async(self, user_id: int) -> CartResponseModel:
        cart = await self.uow.carts.find_cart_with_products_by_user_id_async(user_id)

        if cart == None:
            raise CartNotFoundError(f"Cart for user with id {user_id} not found.")
        
        flat_items = []

        if cart.product_cart is None:
            return CartResponseModel(
                cart_id=cart.id,
                user_id=cart.user_id,
                items=flat_items
            )

        for bridge in cart.product_cart:
            item_in_cart = bridge.product_in_cart
            if not item_in_cart or not item_in_cart.product:
                continue

            product = item_in_cart.product
            
            first_image_url = product.images[0].src if product.images else None

            flat_items.append(
                CartItemResponseModel(
                    product_in_cart_id=item_in_cart.id,
                    product_id=product.id,
                    name=product.name,
                    amount=item_in_cart.amount,
                    price=product.price,
                    image=first_image_url
                )
            )

        return CartResponseModel(
            cart_id=cart.id,
            user_id=cart.user_id,
            items=flat_items
        )

    async def add_product_to_cart_async(self, user_id: int, data: CartAddProductModel) -> None:
        product = await self.uow.carts.find_product_in_cart_async(user_id, data.product_id)

        if product:
            raise ProductAlreadyInCartError(f"Product with id {data.product_id} is already in cart for this user.")

        cart = await self.uow.carts.find_cart_by_user_id_async(user_id)

        if cart == None:
            raise CartNotFoundError(f"Cart for user with id {user_id} not found.")
        
        product_in_cart = await self.uow.carts.save_product_in_cart_async(data)

        await self.uow.carts.save_product_cart_async(cart.id, product_in_cart.id)

    async def remove_product_from_cart_async(self, user_id: int, product_id: int) -> None:
        await self.uow.carts.delete_product_from_cart_async(user_id, product_id)

    async def update_cart_quantity_async(self, user_id: int, product_id: int, new_amount: int, increase: bool) -> CartUpdateResponseModel:        
        if not increase and new_amount < 1:
            await self.uow.carts.delete_product_from_cart_async(user_id, product_id)
            return CartUpdateResponseModel(
                product_id=product_id,
                new_amount=0
            )

        product_in_cart = await self.uow.carts.find_product_in_cart_async(user_id, product_id)

        if product_in_cart == None:
            raise CartNotFoundError(f"Product with id {product_id} not found in cart for user with id {user_id}.")
        
        if increase and product_in_cart.amount + new_amount < 1:
            await self.uow.carts.delete_product_from_cart_async(user_id, product_id)
            return CartUpdateResponseModel(
                product_id=product_id,
                new_amount=0
            )

        product_in_cart = await self.uow.carts.update_cart_quantity_async(product_in_cart, new_amount)

        return CartUpdateResponseModel(
            product_id=product_id,
            new_amount=product_in_cart.amount
        )