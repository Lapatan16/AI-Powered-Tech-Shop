from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .carts_models import CartCreateModel, CartAddProductModel

from ..entities.cart_entity import CartEntity
from ..entities.product_cart_entity import ProductCartEntity
from ..entities.product_in_cart_entity import ProductInCartEntity
from ..entities.product_entity import ProductEntity

class CartsRepository:
    def __init__(self, db_context: AsyncSession):
        self.__db_context = db_context

    async def create_cart_async(self, cart_create_model: CartCreateModel) -> CartEntity:
        new_cart = CartEntity(
            user_id=cart_create_model.user_id
        )

        self.__db_context.add(new_cart)
        await self.__db_context.flush()

        return new_cart
    
    async def delete_cart_async(self, cart_id: int):
        statement = select(CartEntity).where(CartEntity.id == cart_id)
        result = await self.__db_context.execute(statement)
        cart = result.scalars().first()

        if cart:
            await self.__db_context.delete(cart)

    async def find_cart_with_products_by_user_id_async(self, user_id: int) -> CartEntity | None:
        statement = select(CartEntity).where(CartEntity.user_id == user_id).options(
            selectinload(CartEntity.product_cart)
            .selectinload(ProductCartEntity.product_in_cart)
            .selectinload(ProductInCartEntity.product)
            .selectinload(ProductEntity.images)
        )
        result = await self.__db_context.execute(statement)

        return result.scalars().first()
    
    async def find_cart_by_user_id_async(self, user_id: int) -> CartEntity | None:
        statement = select(CartEntity).where(CartEntity.user_id == user_id).options(
            selectinload(CartEntity.product_cart)
            .selectinload(ProductCartEntity.product_in_cart)
        )
        result = await self.__db_context.execute(statement)

        return result.scalars().first()
    
    async def save_product_in_cart_async(self, data: CartAddProductModel):
        new_product_in_cart = ProductInCartEntity(
            product_id=data.product_id,
            amount=data.amount
        )

        self.__db_context.add(new_product_in_cart)
        await self.__db_context.flush()

        return new_product_in_cart
    
    async def save_product_cart_async(self, cart_id: int, product_in_cart_id: int):
        new_product_cart = ProductCartEntity(
            cart_id=cart_id,
            product_in_cart_id=product_in_cart_id
        )

        self.__db_context.add(new_product_cart)
        await self.__db_context.flush()

        return new_product_cart
    
    async def delete_product_from_cart_async(self, user_id: int, product_id: int):
        statement = (
            select(ProductCartEntity)
            .join(ProductCartEntity.product_in_cart)
            .join(ProductCartEntity.cart)
            .where(
                CartEntity.user_id == user_id,
                ProductInCartEntity.product_id == product_id
            )
        )
        result = await self.__db_context.execute(statement)
        product_cart = result.scalars().first()

        if product_cart is None:
            return
        
        await self.__db_context.delete(product_cart)
        await self.__db_context.flush()

    async def find_product_in_cart_async(self, user_id: int, product_id: int) -> ProductInCartEntity | None:
        statement = (
            select(ProductInCartEntity)
            .join(ProductInCartEntity.product_cart)
            .join(ProductCartEntity.cart)
            .where(
                CartEntity.user_id == user_id,
                ProductInCartEntity.product_id == product_id
            ).options(
                selectinload(ProductInCartEntity.product_cart)
                .selectinload(ProductCartEntity.cart)
            )
        )
        result = await self.__db_context.execute(statement)

        return result.scalars().first()

    async def update_cart_quantity_async(self, product_in_cart: ProductInCartEntity, new_amount: int) -> ProductInCartEntity:
        product_in_cart.amount = new_amount
        self.__db_context.add(product_in_cart)
        await self.__db_context.flush()

        return product_in_cart