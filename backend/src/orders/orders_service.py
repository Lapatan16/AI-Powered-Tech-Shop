from fastapi import BackgroundTasks

from .orders_models import OrderResponseModel, OrderItemResponse

from ..database.unit_of_work import UnitOfWork
from ..workers.recommendation_worker import run_single_recommendation_flow

class OrdersService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def checkout_cart_async(self, user_id: int, background_tasks: BackgroundTasks) -> OrderResponseModel:
        cart = await self.uow.carts.find_cart_with_products_by_user_id_async(user_id)
        
        if not cart or not cart.product_cart:
            raise ValueError("Cannot checkout an empty shopping cart configuration.")

        for bridge in cart.product_cart:
            item = bridge.product_in_cart
            if item and item.product:
                if item.product.is_deleted:
                    raise ValueError(f"Product '{item.product.name}' is no longer available in our store catalog.")
                if item.product.stock < item.amount:
                    raise ValueError(f"Insufficient stock for '{item.product.name}'. Available: {item.product.stock}")

        completed_order = await self.uow.orders.create_order_from_cart_async(user_id, cart)

        await self.uow.commit()
        
        background_tasks.add_task(run_single_recommendation_flow, user_id)
        
        return OrderResponseModel(
            order_id=completed_order.id,
            total_price=completed_order.total_price,
            created_at=completed_order.created_at,
            items=[
                OrderItemResponse(
                    product_name=i.product_name,
                    price_at_purchase=i.price_at_purchase,
                    quantity=i.quantity
                ) for i in completed_order.items
            ]
        )