from fastapi import Depends

from .products_service import ProductsService

from ..database.unit_of_work import UnitOfWork

def get_products_service(uow: UnitOfWork = Depends(UnitOfWork.get_unit_of_work)) -> ProductsService:
    return ProductsService(uow)