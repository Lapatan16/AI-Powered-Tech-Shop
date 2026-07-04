from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .order_item_entity import OrderItemEntity

class OrderEntity(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    total_price: float = Field(default=0.0, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    items: List["OrderItemEntity"] = Relationship(back_populates="order", cascade_delete=True)