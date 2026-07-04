from .users_models import DashboardAnalyticsResponse, DashboardCharts, SummaryMetrics, UserResponseModel
from .users_exceptions import *

from ..database.unit_of_work import UnitOfWork

class UsersService():
    
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all_users_async(self) -> list[UserResponseModel]:
        result = await self.uow.users.find_all_users_async()

        return [UserResponseModel.model_validate(user) for user in result]
    
    async def get_user_by_username(self, username: str) -> UserResponseModel | None:
        result = await self.uow.users.find_user_by_username(username)

        if not result:
            raise NotFoundError(f"user with username: {username} not found.")

        return UserResponseModel.model_validate(result)
    
    async def get_user_by_email(self, email: str) -> UserResponseModel:
        result = await self.uow.users.find_user_by_email(email)

        if not result:
            raise NotFoundError(f"user with email: {email} not found.")

        return UserResponseModel.model_validate(result)
    
    async def get_dashboard_analytics_by_user_id_async(self, user_id: int) -> DashboardAnalyticsResponse:
        
        summary = await self.uow.products.get_seller_summary_metrics_async(user_id)
        charts_data = await self.uow.products.get_seller_chart_analytics_async(user_id)
        
        return DashboardAnalyticsResponse(
            summary_metrics=SummaryMetrics(**summary),
            charts=DashboardCharts(**charts_data)
        )