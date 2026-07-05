from ast import List
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from .products_query import ProductQueryParams

from ..entities.sub_category_entity import SubCategoryEntity
from ..entities.product_entity import ProductEntity
from ..entities.category_entity import CategoryEntity
from ..entities.image_entity import ImageEntity
from ..entities.order_item_entity import OrderItemEntity
from ..entities.order_entity import OrderEntity

class ProductsRepository():
    def __init__(self, db_context: AsyncSession):
        self.__db_context = db_context

    async def find_all_products_async(
        self, 
        params: ProductQueryParams
    ) -> tuple[list[ProductEntity], int]:
        
        statement = select(ProductEntity).options(selectinload(ProductEntity.images)).where(ProductEntity.is_deleted == False)

        if params.category_id is not None:
            statement = statement.join(SubCategoryEntity).where(
                SubCategoryEntity.category_id == params.category_id
            )
            
        if params.sub_category_id is not None:
            statement = statement.where(ProductEntity.sub_category_id == params.sub_category_id)

        if params.sort_by_price == "asc":
            statement = statement.order_by(asc(ProductEntity.price))
        elif params.sort_by_price == "desc":
            statement = statement.order_by(desc(ProductEntity.price))
        else:
            statement = statement.order_by(desc(ProductEntity.id))

        count_statement = select(func.count()).select_from(statement.subquery())
        count_result = await self.__db_context.execute(count_statement)
        total_records = count_result.scalar_one()

        statement = statement.offset(params.offset).limit(params.limit)
        result = await self.__db_context.execute(statement)
        entities = result.scalars().all()

        return entities, total_records
    
    async def find_product_by_id_async(self, product_id: int) -> ProductEntity | None:
        statement = (
            select(ProductEntity)
            .where(ProductEntity.id == product_id)
            .options(
                selectinload(ProductEntity.images),
                joinedload(ProductEntity.user),
                joinedload(ProductEntity.sub_category)
                    .joinedload(SubCategoryEntity.category)
            )
        )

        result = await self.__db_context.execute(statement)

        return result.scalars().first()
    
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
    ) -> ProductEntity:
        
        new_product = ProductEntity(
            name=name,
            description=description,
            sub_category_id=sub_category_id,
            user_id=user_id,
            price=price,
            stock=stock,
            discount=discount
        )

        self.__db_context.add(new_product)
        await self.__db_context.flush() 

        for path in image_src_list:
            new_image = ImageEntity(
                src=path,
                product_id=new_product.id
            )
            self.__db_context.add(new_image)

        await self.__db_context.flush()
        
        return new_product
    
    async def delete_product_async(self, product_id: int) -> None:
        statement = select(ProductEntity).where(ProductEntity.id == product_id)

        result = await self.__db_context.execute(statement)
        product = result.scalars().first()

        if product is not None:
            product.is_deleted = True
            self.__db_context.add(product)
            await self.__db_context.flush()

    async def find_product_categories_and_subcategories_async(self) -> list[CategoryEntity]:
        statement = select(CategoryEntity).options(
            selectinload(CategoryEntity.sub_categories)
        )

        result = await self.__db_context.execute(statement)

        return result.scalars().all()
    
    async def find_all_products_by_sub_category_async(self, sub_category_id: int) -> list[ProductEntity]:
        statement = (
            select(ProductEntity)
            .where(ProductEntity.sub_category_id == sub_category_id)
            .options(
                selectinload(ProductEntity.images),
                joinedload(ProductEntity.sub_category)
                    .joinedload(SubCategoryEntity.category)
            )
        )

        result = await self.__db_context.execute(statement)

        return result.scalars().all()
    
    async def get_seller_summary_metrics_async(self, user_id: int) -> dict:
        sales_stmt = (
            select(
                func.coalesce(func.sum(OrderItemEntity.price_at_purchase * OrderItemEntity.quantity), 0.0),
                func.coalesce(func.sum(OrderItemEntity.quantity), 0)
            )
            .join(ProductEntity, OrderItemEntity.product_id == ProductEntity.id)
            .where(ProductEntity.user_id == user_id)
        )
        sales_res = await self.__db_context.execute(sales_stmt)
        total_revenue, units_sold = sales_res.tuples().one()

        inventory_stmt = (
            select(
                func.count(ProductEntity.id),
                func.count(func.nullif(ProductEntity.stock == 0, False))
            )
            .where(ProductEntity.user_id == user_id, ProductEntity.is_deleted == False)
        )
        inventory_res = await self.__db_context.execute(inventory_stmt)
        active_listings, out_of_stock = inventory_res.tuples().one()

        return {
            "total_revenue": float(total_revenue),
            "units_sold": int(units_sold),
            "active_listings_count": int(active_listings),
            "out_of_stock_count": int(out_of_stock)
        }

    async def get_seller_chart_analytics_async(self, user_id: int) -> dict:
        date_trunc = func.to_char(OrderEntity.created_at, 'YYYY-MM-DD')
        trend_stmt = (
            select(
                date_trunc.label("day"),
                func.coalesce(func.sum(OrderItemEntity.price_at_purchase * OrderItemEntity.quantity), 0.0)
            )
            .join(OrderEntity, OrderItemEntity.order_id == OrderEntity.id)
            .join(ProductEntity, OrderItemEntity.product_id == ProductEntity.id)
            .where(ProductEntity.user_id == user_id)
            .group_by(date_trunc)
            .order_by(asc(date_trunc))
        )
        trend_res = await self.__db_context.execute(trend_stmt)
        revenue_trend = [{"date": row[0], "revenue": float(row[1])} for row in trend_res.tuples().all()]

        cat_stmt = (
            select(
                SubCategoryEntity.name,
                func.coalesce(func.sum(OrderItemEntity.price_at_purchase * OrderItemEntity.quantity), 0.0)
            )
            .join(ProductEntity, OrderItemEntity.product_id == ProductEntity.id)
            .join(SubCategoryEntity, ProductEntity.sub_category_id == SubCategoryEntity.id)
            .where(ProductEntity.user_id == user_id)
            .group_by(SubCategoryEntity.name)
        )
        cat_res = await self.__db_context.execute(cat_stmt)
        category_distribution = [{"name": row[0], "value": float(row[1])} for row in cat_res.tuples().all()]

        stock_stmt = (
            select(
                ProductEntity.name,
                func.coalesce(func.sum(OrderItemEntity.quantity), 0).label("sold"),
                ProductEntity.stock
            )
            .join(OrderItemEntity, OrderItemEntity.product_id == ProductEntity.id, isouter=True)
            .where(ProductEntity.user_id == user_id, ProductEntity.is_deleted == False)
            .group_by(ProductEntity.id, ProductEntity.name, ProductEntity.stock)
            .order_by(desc("sold"))
            .limit(5)
        )
        stock_res = await self.__db_context.execute(stock_stmt)
        stock_vs_sales = [{"name": row[0], "sold": int(row[1]), "stock": int(row[2])} for row in stock_res.tuples().all()]

        return {
            "revenue_trend": revenue_trend,
            "category_distribution": category_distribution,
            "stock_vs_sales": stock_vs_sales
        }
    
    async def find_seller_products_paginated_async(
        self, 
        user_id: int, 
        page: int, 
        limit: int
    ) -> tuple[list[ProductEntity], int]:
        offset = (page - 1) * limit
        
        statement = (
            select(ProductEntity)
            .options(selectinload(ProductEntity.images))
            .where(ProductEntity.user_id == user_id, ProductEntity.is_deleted == False)
            .order_by(desc(ProductEntity.id))
        )

        count_statement = select(func.count()).select_from(statement.subquery())
        count_result = await self.__db_context.execute(count_statement)
        total_records = count_result.scalar_one()

        statement = statement.offset(offset).limit(limit)
        result = await self.__db_context.execute(statement)
        entities = result.scalars().all()

        return entities, total_records

    async def update_product_async(
        self, 
        product_id: int, 
        name: str, 
        description: str, 
        sub_category_id: int, 
        price: float, 
        stock: int, 
        discount: float
    ) -> ProductEntity | None:
        statement = select(ProductEntity).where(ProductEntity.id == product_id, ProductEntity.is_deleted == False)
        result = await self.__db_context.execute(statement)
        product = result.scalars().first()

        if product is not None:
            product.name = name
            product.description = description
            product.sub_category_id = sub_category_id
            product.price = price
            product.stock = stock
            product.discount = discount
            
            self.__db_context.add(product)
            await self.__db_context.flush()
            
        return product