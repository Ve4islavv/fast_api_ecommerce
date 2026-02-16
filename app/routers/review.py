from fastapi import APIRouter, Depends, HTTPException
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from starlette import status
from datetime import datetime

from app.models.rating import Rating
from app.schemas import CreateReview
from app.models.review import Review
from app.routers.auth import get_current_user
from app.models.product import Product

router = APIRouter(prefix='/review', tags=['review'])


async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(Rating.grade)).where(
            Rating.product_id == product_id,
            Rating.is_active == True
        )
    )
    avg_rating = result.scalar() or 0

    await db.execute(
        update(Product)
        .where(Product.id == product_id)
        .values(rating=avg_rating)
    )
    await db.commit()


@router.get('/all_review')
async def get_all_review(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    result = reviews.all()
    if not result:
        return []
    return result


@router.post('/create')
async def add_review(
    db: Annotated[AsyncSession, Depends(get_db)],
    new_review: CreateReview,
    user: Annotated[dict, Depends(get_current_user)]
):
    if not user.get('is_active'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not active'
        )

    product = await db.scalar(select(Product).where(Product.id == new_review.product_id))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )

    existing_review = await db.scalar(
        select(Review).where(
            Review.user_id == user.get('id'),
            Review.product_id == new_review.product_id,
            Review.is_active == True
        )
    )
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You have already reviewed this product'
        )

    new_rating = Rating(
        grade=new_review.rating,
        user_id=user.get('id'),
        product_id=new_review.product_id,
        is_active=True
    )
    db.add(new_rating)
    await db.flush()

    new_review_db = Review(
        user_id=user.get('id'),
        product_id=new_review.product_id,
        comment=new_review.comment,
        rating_id=new_rating.id,
        is_active=True,
        comment_date=datetime.now()
    )
    db.add(new_review_db)
    await db.commit()

    await update_product_rating(db, new_review.product_id)

    return {
        'status': status.HTTP_200_OK,
        'detail': 'Review added successfully'
    }


@router.get('/{product_id}')
async def product_reviews(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int
):
    product = await db.scalar(select(Product).where(Product.id == product_id))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )

    reviews = await db.scalars(
        select(Review)
        .where(
            Review.product_id == product_id,
            Review.is_active == True
        )
    )
    result = reviews.all()
    return result


@router.put('/delete/{review_id}')
async def delete_review(
    db: Annotated[AsyncSession, Depends(get_db)],
    review_id: int,
    user: Annotated[dict, Depends(get_current_user)]
):
    if not user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admin can delete reviews'
        )

    review = await db.scalar(
        select(Review)
        .where(
            Review.id == review_id,
            Review.is_active == True
        )
    )

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review not found'
        )

    await db.execute(
        update(Review)
        .where(Review.id == review_id)
        .values(is_active=False)
    )

    await db.execute(
        update(Rating)
        .where(Rating.id == review.rating_id)
        .values(is_active=False)
    )

    await db.commit()

    await update_product_rating(db, review.product_id)

    return {
        'status': status.HTTP_200_OK,
        'detail': 'Review deleted!'
    }

