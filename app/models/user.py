

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from app.backend.db import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String(50), unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_supplier = Column(Boolean, default=False)
    is_customer = Column(Boolean, default=True)

    password = Column(String())

    products = relationship('Product', back_populates='supplier')
    rating = relationship('Rating', back_populates='user')
    review = relationship('Review', back_populates='user')


