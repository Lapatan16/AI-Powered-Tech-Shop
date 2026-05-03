from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
import os
from typing import AsyncGenerator

from ..common.logger import logging

load_dotenv()

__connection_string = os.environ.get("DB_CONNECTION")

if(__connection_string is None):
    logging.error("Database connection string not found in environment.")
    exit()

__engine = create_async_engine(__connection_string)

__AsyncSessionLocal = async_sessionmaker(
    bind=__engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with __AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()