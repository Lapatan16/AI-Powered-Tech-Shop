from typing import Optional, Generic, TypeVar
from pydantic import BaseModel
from fastapi import Query

T = TypeVar('T')

class ProductQueryParams:
    def __init__(
        self,
        category_id: Optional[int] = Query(None, description="Filter by parent category"),
        sub_category_id: Optional[int] = Query(None, description="Filter by subcategory"),
        sort_by_price: Optional[str] = Query(None, pattern="^(asc|desc)$", description="Sort string direction"),
        page: int = Query(1, ge=1),
        limit: int = Query(12, ge=1, le=100)
    ):
        self.category_id = category_id
        self.sub_category_id = sub_category_id
        self.sort_by_price = sort_by_price
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit

class PaginatedEnvelope(BaseModel, Generic[T]):
    items: list[T]
    total_records: int
    page: int
    limit: int
    total_pages: int

class WorkerProductQueryParams:
    def __init__(
        self,
        category_id: Optional[int] = None,
        sub_category_id: Optional[int] = None,
        sort_by_price: Optional[str] = None,
        page: int = 1,
        limit: int = 12
    ):
        self.category_id = category_id
        self.sub_category_id = sub_category_id
        self.sort_by_price = sort_by_price
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit