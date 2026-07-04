from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .order_entity import OrderEntity

class OrderItemEntity(SQLModel, table=True):
    __tablename__ = "order_items"

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    product_id: int | None = Field(foreign_key="products.id", nullable=True)
    
    product_name: str = Field(nullable=False)
    price_at_purchase: float = Field(nullable=False)
    quantity: int = Field(nullable=False)

    order: Optional["OrderEntity"] = Relationship(back_populates="items")