from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB

class RecommendationEntity(SQLModel, table=True):
    __tablename__ = "recommendations"

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    recommended_product_ids: list[int] = Field(sa_column=Column(JSONB, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)