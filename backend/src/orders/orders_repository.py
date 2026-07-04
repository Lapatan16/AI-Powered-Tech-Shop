from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..entities.cart_entity import CartEntity
from ..entities.order_entity import OrderEntity
from ..entities.order_item_entity import OrderItemEntity

class OrdersRepository:
    def __init__(self, db_context: AsyncSession):
        self.__db_context = db_context

    async def create_order_from_cart_async(self, user_id: int, cart: CartEntity) -> OrderEntity:
        grand_total = 0.0
        order_items_to_create = []

        for bridge in cart.product_cart:
            item_in_cart = bridge.product_in_cart
            if not item_in_cart or not item_in_cart.product:
                continue
            
            product = item_in_cart.product
            
            product.stock -= item_in_cart.amount
            self.__db_context.add(product)

            final_price = product.price
            if product.discount > 0:
                final_price = product.price * (1.0 - (product.discount / 100.0))

            item_subtotal = final_price * item_in_cart.amount
            grand_total += item_subtotal

            order_items_to_create.append(
                OrderItemEntity(
                    product_id=product.id,
                    product_name=product.name,
                    price_at_purchase=final_price,
                    quantity=item_in_cart.amount
                )
            )

        new_order = OrderEntity(user_id=user_id, total_price=grand_total)
        self.__db_context.add(new_order)
        await self.__db_context.flush()

        for item in order_items_to_create:
            item.order_id = new_order.id
            self.__db_context.add(item)

        for bridge in cart.product_cart:
            await self.__db_context.delete(bridge)
            if bridge.product_in_cart:
                await self.__db_context.delete(bridge.product_in_cart)

        await self.__db_context.flush()

        statement = (
            select(OrderEntity)
            .where(OrderEntity.id == new_order.id)
            .options(selectinload(OrderEntity.items))
        )
        result = await self.__db_context.execute(statement)
        fully_loaded_order = result.scalars().one()

        return fully_loaded_order