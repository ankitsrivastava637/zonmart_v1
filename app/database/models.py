from pydantic import UUID1
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
import uuid

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"

    id = Column(String, default=str(uuid.uuid4()), primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    version = Column(Integer, default=0, onupdate=0)
    address = Column(Text)

class ProductTable(Base):
    __tablename__ = "products"

    id = Column(String, default=str(uuid.uuid4()), primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)    

class UserCartTable(Base):
    __tablename__ = "user_carts"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)

class OrderTable(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    product_id = Column(String, index=True)
    quantity = Column(Integer)
    order_date = Column(TIMESTAMP)
    status = Column(String, default="active")


