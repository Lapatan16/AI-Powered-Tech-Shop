from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .sub_category_entity import SubCategoryEntity

class CategoryEntity(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    sub_categories: List["SubCategoryEntity"] = Relationship(back_populates="category")