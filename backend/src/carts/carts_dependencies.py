from fastapi import Depends

from .carts_service import CartsService

from ..database.unit_of_work import UnitOfWork

def get_carts_service(uow: UnitOfWork = Depends(UnitOfWork.get_unit_of_work)) -> CartsService:
    return CartsService(uow)