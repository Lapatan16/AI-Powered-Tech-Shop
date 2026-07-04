from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
import os
from typing import AsyncGenerator

from ..common.logger import logging
from ..entities.user_entity import UserEntity
from ..entities.product_entity import ProductEntity
from ..entities.category_entity import CategoryEntity
from ..entities.product_in_cart_entity import ProductInCartEntity
from ..entities.image_entity import ImageEntity
from ..entities.product_cart_entity import ProductCartEntity
from ..entities.cart_entity import CartEntity
from ..entities.discount_entity import DiscountEntity
from ..entities.sub_category_entity import SubCategoryEntity
from ..entities.order_entity import OrderEntity
from ..entities.order_item_entity import OrderItemEntity
from ..entities.recommendation_entity import RecommendationEntity

load_dotenv()

__connection_string = os.environ.get("DB_CONNECTION")

if(__connection_string is None):
    logging.error("Database connection string not found in environment.")
    exit()

__engine = create_async_engine(__connection_string)

AsyncSessionLocal = async_sessionmaker(
    bind=__engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()