from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..entities.recommendation_entity import RecommendationEntity
from ..entities.product_entity import ProductEntity

class RecommendationsRepository:
    def __init__(self, db_context: AsyncSession):
        self.__db_context = db_context

    async def get_recommended_products_by_user_id_async(self, user_id: int) -> list[ProductEntity]:
        statement = select(RecommendationEntity).where(RecommendationEntity.user_id == user_id)
        result = await self.__db_context.execute(statement)
        recommendation = result.scalars().first()

        if not recommendation or not recommendation.recommended_product_ids:
            return []

        product_stmt = (
            select(ProductEntity)
            .where(
                ProductEntity.id.in_(recommendation.recommended_product_ids),
                ProductEntity.is_deleted == False
            )
            .options(selectinload(ProductEntity.images))
        )
        product_result = await self.__db_context.execute(product_stmt)
        products = product_result.scalars().all()

        order_map = {pid: index for index, pid in enumerate(recommendation.recommended_product_ids)}
        return sorted(products, key=lambda p: order_map.get(p.id, 999))

    async def get_default_top_products_async(self, limit: int = 8) -> list[ProductEntity]:
        statement = (
            select(ProductEntity)
            .where(ProductEntity.is_deleted == False)
            .order_by(desc(ProductEntity.id))
            .limit(limit)
            .options(selectinload(ProductEntity.images))
        )
        result = await self.__db_context.execute(statement)
        return list(result.scalars().all())