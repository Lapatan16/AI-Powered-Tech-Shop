from pydantic import BaseModel
from datetime import datetime

class OrderItemResponse(BaseModel):
    product_name: str
    price_at_purchase: float
    quantity: int

class OrderResponseModel(BaseModel):
    order_id: int
    total_price: float
    created_at: datetime
    items: list[OrderItemResponse]