from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))  # Şifreyi hash'leyeceğiz
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # User'ın ürünleri ile ilişki
    products = relationship("Product", back_populates="owner")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_type = Column(String(50), index=True)
    name = Column(String(100), index=True)
    quantity = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Product'ın sahibi ile ilişki
    owner = relationship("User", back_populates="products") 