from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .product_entity import ProductEntity
    from .product_cart_entity import ProductCartEntity

class ProductInCartEntity(SQLModel, table=True):
    __tablename__="product_in_cart"

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", nullable=False, index=True)
    amount: int = Field(nullable=False)

    product: Optional["ProductEntity"] = Relationship(back_populates="product_in_cart")
    product_cart: Optional["ProductCartEntity"] = Relationship(back_populates="product_in_cart")