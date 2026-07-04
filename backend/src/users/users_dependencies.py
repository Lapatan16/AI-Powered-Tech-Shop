from fastapi import Depends

from .users_service import UsersService

from ..database.unit_of_work import UnitOfWork

def get_users_service(uow: UnitOfWork = Depends(UnitOfWork.get_unit_of_work)) -> UsersService:
    return UsersService(uow)