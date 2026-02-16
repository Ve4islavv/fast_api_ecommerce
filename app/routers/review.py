from fastapi import APIRouter, Depends, HTTPException
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, join
from starlette import status

from app.models.rating import Rating
from app.schemas import CreateReview
from app.models.review import Review
from app.routers.auth import get_current_user
from app.models import *
from datetime import datetime

router = APIRouter(prefix='/review', tags=['review'])

@router.get('/all_review')
async def get_all_review(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    if reviews is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Reviews not found')
    return reviews.all()

@router.post('/create')
async def add_review(db: Annotated[AsyncSession, Depends(get_db)],
                        new_review: CreateReview,
                     user: Annotated[dict, (get_current_user)]):
    if user.get('is_active'):
        await db.execute(insert(Review).values(user_id=user.get('id'),
                                               product_id=new_review.product_id,
                                               comment=new_review.comment,
                                               rating_id=new_review.rating,
                                               is_active=True,
                                               comment_date = datetime.now()))

@router.get('/{product_id}')
async def product_reviews(db: Annotated[AsyncSession, Depends(get_db)],
                          product_id: int):
    reviews = await db.scalars(select(Review).where(Review.product_id == product_id,
                                                    Review.is_active == True))
    if reviews is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail='Reviews not found')
    return reviews.all()


@router.put('/delete/{review_id}')
async def delete_review(db: Annotated[AsyncSession, Depends(get_db)],
                        review_id: int,
                        user: Annotated[dict, Depends(get_current_user)]):
    review = await db.scalar(select(Review).where(Review.id == review_id,
                                                  Review.is_active == True))
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Review not foud')
    if not user.get('is_admin'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Only admin user can delete review')
    await db.execute(update(Review).where(Review.id == review_id).values(is_active=False))
    await db.commit()
    return {'status': status.HTTP_200_OK,
            'detail': 'Review deleted!'}