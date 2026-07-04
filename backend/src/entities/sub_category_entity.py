from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .category_entity import CategoryEntity
    from .product_entity import ProductEntity

class SubCategoryEntity(SQLModel, table=True):
    __tablename__ = "sub_categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    category_id: int = Field(foreign_key="categories.id", nullable=False)

    category: Optional["CategoryEntity"] = Relationship(back_populates="sub_categories")
    products: List["ProductEntity"] = Relationship(back_populates="sub_category")