from sqlmodel import Field, SQLModel

class UserEntity(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True, nullable=False, index=True)
    email: str = Field(unique=True, nullable=False, index=True)
    password: str = Field(nullable=False)