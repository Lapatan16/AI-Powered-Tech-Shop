from pydantic import BaseModel, Field
from typing import List

class CartCreateModel(BaseModel):
    user_id: int = Field()

class CartMinResponseModel(BaseModel):
    id: int = Field()
    user_id: int = Field()

class CartItemResponseModel(BaseModel):
    product_in_cart_id: int = Field()
    product_id: int = Field()
    name: str = Field()
    amount: int = Field()
    price: float = Field()
    image: str | None = Field(default=None)

class CartResponseModel(BaseModel):
    cart_id: int = Field()
    user_id: int = Field()
    items: List[CartItemResponseModel] = Field()

class CartAddProductModel(BaseModel):
    product_id: int = Field()
    amount: int = Field()

class CartUpdateResponseModel(BaseModel):
    product_id: int = Field()
    new_amount: int = Field()

class CartUpdateModel(BaseModel):
    product_id: int = Field()
    new_amount: int = Field()
    increase: bool = Field()