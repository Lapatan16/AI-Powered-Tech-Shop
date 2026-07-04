from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from .db import get_db, AsyncGenerator

from ..users.users_repository import UsersRepository
from ..auth.auth_repository import AuthRepository
from ..products.products_repository import ProductsRepository
from ..carts.carts_repository import CartsRepository
from ..orders.orders_repository import OrdersRepository
from ..recommendations.recommendations_repository import RecommendationsRepository

class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.__session = session
        
        self.auth = AuthRepository(self.__session)
        self.users = UsersRepository(self.__session)
        self.products = ProductsRepository(self.__session)
        self.carts = CartsRepository(self.__session)
        self.orders = OrdersRepository(self.__session)
        self.recommendations = RecommendationsRepository(self.__session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.__session.rollback()
        else:
            await self.__session.commit()

        return False
    
    async def commit(self):
        await self.__session.commit()

    async def get_unit_of_work(session: AsyncSession = Depends(get_db)) -> AsyncGenerator[UnitOfWork, None]:
        async with UnitOfWork(session) as uow:
            yield uow