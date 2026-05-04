from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .product_entity import ProductEntity
    from .cart_entity import CartEntity

class UserEntity(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True, nullable=False, index=True)
    email: str = Field(unique=True, nullable=False, index=True)
    password: str = Field(nullable=False)

    products: List["ProductEntity"] = Relationship(back_populates="user")
    cart: Optional["CartEntity"] = Relationship(back_populates="user")