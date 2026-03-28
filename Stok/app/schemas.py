from pydantic import BaseModel


class RegisterSchema(BaseModel):
    email: str
    password: str
    company_name: str


class LoginSchema(BaseModel):
    email: str
    password: str


class ProductSchema(BaseModel):
    name: str
    stock_quantity: int
    min_stock: int
    unit: str


class StockSchema(BaseModel):
    product_id: int
    quantity: int