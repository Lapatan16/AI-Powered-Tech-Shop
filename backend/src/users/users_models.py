from pydantic import BaseModel, Field

class UserCreateModel(BaseModel):
    user_name: str = Field()
    email: str = Field()
    password: str = Field()

class UserResponseModel(BaseModel):
    id: int = Field()
    user_name: str = Field()
    email: str = Field()

    model_config = {
        "from_attributes": True
    }

class SummaryMetrics(BaseModel):
    total_revenue: float
    units_sold: int
    active_listings_count: int
    out_of_stock_count: int

class RevenueTrendPoint(BaseModel):
    date: str
    revenue: float

class CategoryDistributionPoint(BaseModel):
    name: str
    value: float

class StockVsSalesPoint(BaseModel):
    name: str
    sold: int
    stock: int

class DashboardCharts(BaseModel):
    revenue_trend: list[RevenueTrendPoint]
    category_distribution: list[CategoryDistributionPoint]
    stock_vs_sales: list[StockVsSalesPoint]

class DashboardAnalyticsResponse(BaseModel):
    summary_metrics: SummaryMetrics
    charts: DashboardCharts