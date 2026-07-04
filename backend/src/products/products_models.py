from typing import List, Optional
from pydantic import BaseModel, Field

from ..entities.category_entity import CategoryEntity
from ..entities.product_entity import ProductEntity

class ProductsPreviewModel(BaseModel):
    id: int | None = Field()
    name: str = Field()
    sub_category_id: int = Field()
    user_id: int = Field()
    price: float = Field()
    stock: int = Field()
    discount: float = Field()
    image: str = Field()

    @classmethod
    def from_entity(cls, entity: ProductEntity) -> "ProductsPreviewModel":        
        first_image_src = entity.images[0].src if entity.images else None

        return cls(
            id=entity.id,
            name=entity.name,
            sub_category_id=entity.sub_category_id,
            user_id=entity.user_id,
            price=entity.price,
            stock=entity.stock,
            discount=entity.discount,
            image=first_image_src
        )
    
class UserMinModel(BaseModel):
    id: int
    user_name: str
    email: str

class CategoryMinModel(BaseModel):
    id: int
    name: str

class SubCategoryDetailsModel(BaseModel):
    id: int
    name: str
    category: CategoryMinModel

class ProductDetailsModel(BaseModel):
    id: Optional[int] = Field(None)
    name: str = Field()
    description: str = Field()
    price: float = Field()
    stock: int = Field()
    discount: float = Field(default=0.0)
    images: List[str] = Field(default_factory=list)
    
    seller: UserMinModel = Field(...)
    sub_category: SubCategoryDetailsModel = Field(...)

    @classmethod
    def from_entity(cls, entity: ProductEntity) -> "ProductDetailsModel":
        image_sources = [image.src for image in entity.images] if entity.images else []

        seller_dto = UserMinModel(
            id=entity.user.id,
            user_name=entity.user.user_name,
            email=entity.user.email
        ) if entity.user else None

        sub_cat_dto = None
        if entity.sub_category:
            category_dto = CategoryMinModel(
                id=entity.sub_category.category.id,
                name=entity.sub_category.category.name
            ) if entity.sub_category.category else None

            sub_cat_dto = SubCategoryDetailsModel(
                id=entity.sub_category.id,
                name=entity.sub_category.name,
                category=category_dto
            )

        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            price=entity.price,
            stock=entity.stock,
            discount=entity.discount,
            images=image_sources,
            seller=seller_dto,
            sub_category=sub_cat_dto
        )
    
class ProductsCreateModel(BaseModel):
    name: str = Field()
    description: str = Field()
    sub_category_id: int = Field()
    user_id: int = Field()
    price: float = Field()
    stock: int = Field()
    discount: float = Field(default=0.0)

class ProductsMinimalModel(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, entity: ProductEntity) -> "ProductsMinimalModel":
        return cls(
            id=entity.id,
            name=entity.name
        )
    
class SubCategoryResponseModel(BaseModel):
    id: int
    name: str
    
class CategoryResponseModel(BaseModel):
    id: int
    name: str
    sub_categories: List[SubCategoryResponseModel] = Field(default_factory=list)

    @classmethod
    def from_entity(cls, entity: "CategoryEntity") -> "CategoryResponseModel":
        sub_categories_dto = [
            SubCategoryResponseModel(
                id=sub_cat.id,
                name=sub_cat.name
            ) for sub_cat in entity.sub_categories
        ] if entity.sub_categories else []

        return cls(
            id=entity.id,
            name=entity.name,
            sub_categories=sub_categories_dto
        )