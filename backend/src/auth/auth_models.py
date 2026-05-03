from pydantic import BaseModel, Field

class LoginAuthModel(BaseModel):
    username: str = Field()
    password: str = Field()

class AccessTokenResponseModel(BaseModel):
    access_token: str = Field()
    token_type: str = Field(default="bearer")

