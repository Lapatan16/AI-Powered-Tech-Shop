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