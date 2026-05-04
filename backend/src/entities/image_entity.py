from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .product_entity import ProductEntity

class ImageEntity(SQLModel, table=True):
    __tablename__="images"

    id: int | None = Field(default=None, primary_key=True)
    src: str = Field(nullable=False)
    product_id: int = Field(foreign_key="products.id", nullable=False, index=True)

    product: Optional["ProductEntity"] = Relationship(back_populates="images")