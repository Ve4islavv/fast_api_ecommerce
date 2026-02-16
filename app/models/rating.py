from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean, Float
from sqlalchemy.orm import relationship



class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    is_active = Column(Boolean, default=True)

    products = relationship('Product', back_populates='rating')
    user = relationship('User', back_populates='rating')
    review = relationship('Review', back_populates='rating', uselist=False)

