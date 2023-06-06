from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

class ProductBase(BaseModel):
    product_name: str
    product_price: float
    product_quantity: int

class ProductCreate(ProductBase):
    pass

class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str

class UserLogin(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_created_at: datetime
    class Config:
        orm_mode = True

class ProductResponse(ProductBase):
    product_id: int
    product_name: str
    product_price: float
    product_quantity: int
    product_created_at: datetime
    user: UserResponse
    class Config:
        orm_mode = True

class CustomerCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr

class CustomerResponse(BaseModel):
    customer_id: int
    customer_name: str
    customer_email: EmailStr
    customer_created_at: datetime
    user: UserResponse
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None

class ReceiptItemCreate(BaseModel):
    product_id: int
    quantity: int

class ReceiptCreate(BaseModel):
    user_id_fk: int
    items: List[ReceiptItemCreate]

class ReceiptItemResponse(BaseModel):
    # id: int
    product_id_fk: int
    product_name: str
    quantity: int
    price: float
    class Config:
        orm_mode = True

class ReceiptResponse(BaseModel):
    receipt_id: int
    user_id_fk: int
    receipt_items: List[ReceiptItemResponse]
    class Config:
        orm_mode = True

class ReceiptResponseTotal(BaseModel):
    receipt_id: int
    user_id_fk: int
    receipt_items: List[ReceiptItemResponse]
    total: float
    class Config:
        orm_mode = True
