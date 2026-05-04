from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .product_entity import ProductEntity

class DiscountEntity(SQLModel, table=True):
    __tablename__="discounts"

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", nullable=False, index=True)
    amount: float = Field(default=0.0, nullable=False)
    start_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False, index=True
    )
    end_date: datetime = Field(nullable=False, index=True)

    product: Optional["ProductEntity"] = Relationship(back_populates="discounts")