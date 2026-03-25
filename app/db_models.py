from sqlalchemy import Column, String, Integer, Float
from app.database import Base


class ProductDB(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


class UserDB(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user")