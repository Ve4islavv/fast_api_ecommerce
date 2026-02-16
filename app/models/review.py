from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    rating_id = Column(Integer, ForeignKey('rating.id'))
    comment = Column(String(200))
    comment_date = Column(DateTime, default=datetime.utcnow())
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='review')
    product = relationship('Product', back_populates='review')
    rating = relationship('Rating', back_populates='review')

