from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr

# Сначала все схемы для Rating
class RatingBase(BaseModel):
    grade: int

class CreateRating(RatingBase):
    pass

class ResponseRating(RatingBase):
    id: int
    user_id: int
    product_id: int
    is_active: bool

# Потом схема для Review, которая использует ResponseRating
class CreateReview(BaseModel):
    product_id: int
    rating: int
    comment: str

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating_id: int
    comment_date: datetime
    rating: ResponseRating  # Теперь ResponseRating уже определен

# Затем остальные схемы
class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category_id: int

class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class ProductWithReview(BaseModel):
    id: int
    name: str
    slug: str
    rating: float
    reviews: List[ReviewResponse] = []