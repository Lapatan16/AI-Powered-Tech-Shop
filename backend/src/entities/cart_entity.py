from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user_entity import UserEntity
    from .product_cart_entity import ProductCartEntity

class CartEntity(SQLModel, table=True):
    __tablename__="carts"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)

    user: Optional["UserEntity"] = Relationship(back_populates="cart")
    product_cart: Optional["ProductCartEntity"] = Relationship(back_populates="product_cart")