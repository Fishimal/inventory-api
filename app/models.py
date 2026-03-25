from pydantic import BaseModel, Field
from typing import List

class Product(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float


class ProductList(BaseModel):
    products: List[Product]


class ProductResponse(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True


class Order(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"   # default role


class UserResponse(BaseModel):
    username: str

    class Config:
        from_attributes = True