import json
import asyncio
import os
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from google import genai
from pydantic import BaseModel, Field

from ..database.db import get_db
from ..database.unit_of_work import UnitOfWork
from ..entities.order_entity import OrderEntity
from ..entities.order_item_entity import OrderItemEntity
from ..entities.recommendation_entity import RecommendationEntity
from ..products.products_query import WorkerProductQueryParams

class AIRecommendationsOutput(BaseModel):
    recommended_product_ids: list[int] = Field(description="Exactly 8 unique active product IDs.")


async def build_recommendations_for_user(session, user_id: int, catalog_data: list[dict]):
    try:
        order_stmt = select(OrderItemEntity).join(OrderEntity).where(OrderEntity.user_id == user_id)
        order_result = await session.execute(order_stmt)
        history = [{"name": i.product_name, "id": i.product_id} for i in order_result.scalars().all()]
        
        if not history:
            return 

        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        prompt = f"""
        Analyze the customer's purchase history and select 8 complementary products from our active store catalog.
        Output EXACTLY 8 product IDs.
        
        History: {json.dumps(history)}
        Catalog: {json.dumps(catalog_data)}
        """
        
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json", "response_schema": AIRecommendationsOutput}
        )
        raw_ids = json.loads(response.text)["recommended_product_ids"]
        
        upsert_stmt = insert(RecommendationEntity).values(
            user_id=user_id,
            recommended_product_ids=raw_ids
        ).on_conflict_do_update(
            index_elements=['user_id'],
            set_={'recommended_product_ids': raw_ids}
        )
        await session.execute(upsert_stmt)
        
    except Exception as e:
        print(f"Failed rendering recommendations profile for user {user_id}: {str(e)}")


async def run_single_recommendation_flow(user_id: int):
    async for session in get_db():
        async with UnitOfWork(session) as uow:
            
            params = WorkerProductQueryParams(limit=1000, page=1)
            
            products, _ = await uow.products.find_all_products_async(params)
            catalog_data = [
                {"id": p.id, "name": p.name, "description": p.description} 
                for p in products if p.stock > 0 and not p.is_deleted
            ]
            
            await build_recommendations_for_user(session, user_id, catalog_data)
        break


async def run_recommendation_cron_worker():
    async for session in get_db():
        async with UnitOfWork(session) as uow:
            from ..products.products_query import ProductQueryParams
            params = ProductQueryParams(limit=1000, page=1)
            products, _ = await uow.products.find_all_products_async(params)
            catalog_data = [
                {"id": p.id, "name": p.name, "description": p.description} 
                for p in products if p.stock > 0 and not p.is_deleted
            ]
            
            user_stmt = select(OrderEntity.user_id).distinct()
            user_res = await session.execute(user_stmt)
            active_user_ids = user_res.scalars().all()
        break

    for uid in active_user_ids:
        await run_single_recommendation_flow(uid)


if __name__ == "__main__":
    asyncio.run(run_recommendation_cron_worker())