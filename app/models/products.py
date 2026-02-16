from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, Float
from app.backend.db import Base
from sqlalchemy.orm import relationship
from app.models import *




class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))
    rating = Column(Float)
    is_active = Column(Boolean, default=True)
    supplier_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    category = relationship('Category', back_populates='products')
    supplier = relationship("User", back_populates="products")

