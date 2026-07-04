from typing import List

from .products_query import ProductQueryParams
from .products_exceptions import ProductNotFoundError
from .products_models import (
    ProductDetailsModel,
    ProductsPreviewModel,
    ProductsMinimalModel,
    CategoryResponseModel
)

from ..database.unit_of_work import UnitOfWork

class ProductsService():
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all_products_async(
        self, 
        params: ProductQueryParams
    ) -> tuple[list[ProductsPreviewModel], int]:
        entities, total_records = await self.uow.products.find_all_products_async(params)

        models = [ProductsPreviewModel.from_entity(entity) for entity in entities]
        return models, total_records
    
    async def get_product_by_id_async(self, product_id: int) -> ProductDetailsModel:
        data = await self.uow.products.find_product_by_id_async(product_id)

        if data is None:
            raise ProductNotFoundError(f"Product with id {product_id} not found")

        return ProductDetailsModel.from_entity(data)
    
    async def create_product_async(
        self, 
        name: str,
        description: str,
        sub_category_id: int,
        user_id: int,
        price: float,
        stock: int,
        discount: float,
        image_src_list: List[str]
    ) -> ProductsMinimalModel:
        
        new_product = await self.uow.products.create_product_async(
            name=name,
            description=description,
            sub_category_id=sub_category_id,
            user_id=user_id,
            price=price,
            stock=stock,
            discount=discount,
            image_src_list=image_src_list
        )

        return ProductsMinimalModel.from_entity(new_product)
        
    async def delete_product_async(self, product_id: int) -> None:
        await self.uow.products.delete_product_async(product_id)

    async def get_product_categories_and_subcategories_async(self) -> list[CategoryResponseModel]:
        categories = await self.uow.products.find_product_categories_and_subcategories_async()

        return [CategoryResponseModel.from_entity(category) for category in categories]