from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .product_cart_entity import ProductCartEntity
    from .cart_entity import CartEntity

class ProductCartEntity(SQLModel, table=True):
    __tablename__="product_cart"

    product_in_cart_id: int = Field(foreign_key="product_in_cart.id", primary_key=True)
    cart_id: int = Field(foreign_key="carts.id", primary_key=True)

    product_in_cart: Optional["ProductCartEntity"] = Relationship(back_populates="product_cart")
    cart: Optional["CartEntity"] = Relationship(back_populates="product_cart")
