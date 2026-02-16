from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, Float
from app.backend.db import Base
from sqlalchemy.orm import relationship
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from fastapi import Depends




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
    rating = relationship('Rating', back_populates='products')
    review = relationship('Review', back_populates='product')


    async def update_rating(self,
                            db: Annotated[AsyncSession, Depends(get_db)]):
        from sqlalchemy import func, select
        from app.models.rating import Rating
        result = await  db.scalar(select(func.avg(Rating.grade)).where(
            Rating.id == self.id,
            Rating.is_active == True))
        self.rating = round(result, 2) if result else 0.0
        await db.commit()