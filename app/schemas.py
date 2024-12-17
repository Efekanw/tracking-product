from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    product_type: str
    name: str
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str