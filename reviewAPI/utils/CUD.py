from fastapi import HTTPException, Depends
from sqlalchemy import select
from model.models import ReviewORM,CreatedReview, UpdatedReview,DeletedReview
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db

async def create_review(cr:CreatedReview, db: AsyncSession = Depends(get_db)):
  new_review = ReviewORM(content_index = cr.content_index, user_id = cr.user_id, review = cr.review)
  db.add(new_review)
  await db.commit()
  await db.refresh(new_review) 
  return new_review

async def update_review(ur:UpdatedReview, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(ReviewORM).where(ReviewORM.review_index == ur.review_index))
  new_review = result.scalar_one_or_none()
  if new_review is None:
    raise HTTPException(status_code=404, detail="Review not found")
  new_review.review = ur.review
  await db.commit()
  return new_review

async def delete_review(dr:DeletedReview, db: AsyncSession = Depends(get_db)):
  # users 테이블에서 모든 행 선택
  result = await db.execute(select(ReviewORM).where(ReviewORM.review_index == dr.review_index))
  new_review = result.scalar_one_or_none()
  if new_review is None:
      raise HTTPException(status_code=404, detail="Review not found")
  await db.delete(new_review)
  await db.commit()
  return new_review
