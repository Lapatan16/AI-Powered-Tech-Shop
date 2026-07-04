from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .product_entity import ProductEntity

class DiscountEntity(SQLModel, table=True):
    __tablename__="discounts"

    id: int | None = Field(default=None, primary_key=True)
    amount: float = Field(default=0.0, nullable=False)
    start_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False, index=True
    )
    end_date: datetime = Field(nullable=False, index=True)

    # product: Optional["ProductEntity"] = Relationship(back_populates="discount") - deleted because it breaks the product

# --- IGNORE ---
# deleted because of changes in the product entity and product creation process. Discount is now a simple float field in the product entity, not a separate entity.