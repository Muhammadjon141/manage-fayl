from pydantic import BaseModel
from typing import List, Optional

class RegisterModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
                "id": 1,
                "username": "admin",
                "email": "admin@gmail.com",
                "password": "7982",
                "is_staff": False,
                "is_active": True
        }
    

class LoginModel(BaseModel):
    username: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "username": "admin",
            "password": "7982",
        }
        
class ProductListModel(BaseModel):
    name: Optional[str]
    price: Optional[int]
    class Config:
        orm_mode = True
        schema_extra = {
            "name": "banan",
            "price": 15,
        }

class ProductModel(BaseModel):
    name: Optional[str]
    price: Optional[int]
    class Config:
        orm_mode = True
        schema_extra = {
            "name": "banan",
            "price": 15,
        }

class OrderListModel(BaseModel):
    id: Optional[int]
    quantity: Optional[int]
    order_status: Optional[str]
    user_id: Optional[int]
    product_id: Optional[int]
    # class Config:
    #     orm_mode = True
    #     schema_extra = {
    #         "name": "banan",
    #         "price": 15,
    #     }

class UserOrdersListModel(BaseModel):
    id: Optional[int]