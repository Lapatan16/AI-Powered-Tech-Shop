from typing import List

from .products_query import ProductQueryParams
from .products_exceptions import ProductNotFoundError
from .products_models import (
    ProductDetailsModel,
    ProductsPreviewModel,
    ProductsMinimalModel,
    CategoryResponseModel,
    ProductsUpdateModel
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

    async def get_product_categories_and_subcategories_async(self) -> list[CategoryResponseModel]:
        categories = await self.uow.products.find_product_categories_and_subcategories_async()

        return [CategoryResponseModel.from_entity(category) for category in categories]
    
    async def get_seller_products_async(
        self, 
        user_id: int, 
        page: int, 
        limit: int
    ) -> tuple[list[ProductsPreviewModel], int]:
        entities, total_records = await self.uow.products.find_seller_products_paginated_async(user_id, page, limit)
        models = [ProductsPreviewModel.from_entity(entity) for entity in entities]
        return models, total_records

    async def update_product_async(
        self, 
        product_id: int, 
        user_id: int, 
        model: ProductsUpdateModel
    ) -> ProductsMinimalModel:
        product = await self.uow.products.find_product_by_id_async(product_id)
        
        if product is None or product.is_deleted:
            raise ProductNotFoundError(f"Product with id {product_id} not found")
            
        if product.user_id != user_id:
            raise PermissionError("You do not own this product listing.")

        updated_entity = await self.uow.products.update_product_async(
            product_id=product_id,
            name=model.name,
            description=model.description,
            sub_category_id=model.sub_category_id,
            price=model.price,
            stock=model.stock,
            discount=model.discount
        )
        return ProductsMinimalModel.from_entity(updated_entity)

    async def delete_product_secure_async(self, product_id: int, user_id: int) -> None:
        product = await self.uow.products.find_product_by_id_async(product_id)
        
        if product is None or product.is_deleted:
            raise ProductNotFoundError(f"Product with id {product_id} not found")
            
        if product.user_id != user_id:
            raise PermissionError("You do not own this product listing.")
            
        await self.uow.products.delete_product_async(product_id)