from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .category_entity import CategoryEntity
    from .user_entity import UserEntity
    from .image_entity import ImageEntity
    from .product_in_cart_entity import ProductInCartEntity
    from .discount_entity import DiscountEntity

class ProductEntity(SQLModel, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(default="", nullable=False)
    category_id: int = Field(foreign_key="categories.id", nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    price: float = Field(default=0.0, nullable=False)
    stock: int = Field(default=0, nullable=False)

    category: Optional["CategoryEntity"] = Relationship(back_populates="products")
    user: Optional["UserEntity"] = Relationship(back_populates="products")
    images: List["ImageEntity"] = Relationship(back_populates="product")
    product_in_cart: List["ProductInCartEntity"] = Relationship(back_populates="product")
    discounts: List["DiscountEntity"] = Relationship(back_populates="product")