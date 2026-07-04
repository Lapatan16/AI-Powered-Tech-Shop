from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .product_in_cart_entity import ProductInCartEntity
    from .cart_entity import CartEntity

class ProductCartEntity(SQLModel, table=True):
    __tablename__="product_cart"

    product_in_cart_id: int = Field(
        foreign_key="product_in_cart.id",
        primary_key=True,
        ondelete="CASCADE"
    )
    cart_id: int = Field(foreign_key="carts.id", primary_key=True)

    product_in_cart: Optional["ProductInCartEntity"] = Relationship(
        back_populates="product_cart", 
        sa_relationship_kwargs={"passive_deletes": True}
    )
    cart: Optional["CartEntity"] = Relationship(back_populates="product_cart")
