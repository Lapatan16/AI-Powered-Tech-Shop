from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .product_entity import ProductEntity

class CategoryEntity(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    products: List["ProductEntity"] = Relationship(back_populates="category")