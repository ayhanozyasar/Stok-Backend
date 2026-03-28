from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .db import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    plan = Column(String, default="free")
    subscription_active = Column(Boolean, default=False)

    max_users = Column(Integer, default=2)
    max_products = Column(Integer, default=10)

    trial_end = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))

    users = relationship("User", back_populates="company")
    products = relationship("Product", back_populates="company")
    subscription_status = Column(String, default="active")  # active, past_due, canceled


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="admin")

    is_verified = Column(Boolean, default=False)
    reset_token = Column(String, nullable=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    stock_quantity = Column(Integer, default=0)
    min_stock = Column(Integer, default=5)
    unit = Column(String)

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="products")


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    type = Column(String)
    quantity = Column(Integer)

    company_id = Column(Integer)
    user_id = Column(Integer)

    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)