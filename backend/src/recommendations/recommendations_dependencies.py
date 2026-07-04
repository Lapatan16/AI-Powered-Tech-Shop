from fastapi import Depends

from .recommendations_service import RecommendationsService

from ..database.unit_of_work import UnitOfWork

def get_rec_service(uow: UnitOfWork = Depends(UnitOfWork.get_unit_of_work)) -> RecommendationsService:
    return RecommendationsService(uow)    