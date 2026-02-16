from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, Float
from app.backend.db import Base
from sqlalchemy.orm import relationship

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
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    supplier_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Relationships - ИСПРАВЛЕНО
    category = relationship('Category', back_populates='products')
    supplier = relationship("User", back_populates="products")
    ratings = relationship('Rating', back_populates='product', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='product', cascade='all, delete-orphan')