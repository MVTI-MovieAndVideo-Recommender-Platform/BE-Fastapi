from fastapi import HTTPException, Depends
from sqlalchemy import select
from model.models import RatingORM,CreatedRating, UpdatedRating,DeletedRating, PreferenceORM, CreatedPreference, DeletedPreference
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db

async def create_rating(cs:CreatedRating, db: AsyncSession = Depends(get_db)):
  new_rating = RatingORM(media_id = cs.media_id, user_id = cs.user_id, rating = cs.rating)
  db.add(new_rating)
  await db.commit()
  await db.refresh(new_rating) 
  return new_rating

async def update_rating(us:UpdatedRating, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(RatingORM).where(RatingORM.rating_id == us.rating_id))
  new_rating = result.scalar_one_or_none()
  if new_rating is None:
    raise HTTPException(status_code=404, detail="rating not found")
  new_rating.rating = us.rating
  await db.commit()
  return new_rating

async def delete_rating(ds:DeletedRating, db: AsyncSession = Depends(get_db)):
  # users 테이블에서 모든 행 선택
  result = await db.execute(select(RatingORM).where(RatingORM.rating_id == ds.rating_id))
  new_rating = result.scalar_one_or_none()
  if new_rating is None:
      raise HTTPException(status_code=404, detail="rating not found")
  await db.delete(new_rating)
  await db.commit()
  return new_rating

async def create_preference(cl:CreatedPreference, db: AsyncSession = Depends(get_db)):
  new_rating = PreferenceORM(content_index = cl.content_index, user_id = cl.user_id)
  db.add(new_rating)
  await db.commit()
  await db.refresh(new_rating) 
  return new_rating

async def delete_preference(dl:DeletedPreference, db: AsyncSession = Depends(get_db)):
  # users 테이블에서 모든 행 선택
  result = await db.execute(select(PreferenceORM).where(PreferenceORM.preference_index == dl.preference_index))
  new_preference = result.scalar_one_or_none()
  if new_preference is None:
      raise HTTPException(status_code=404, detail="preference not found")
  await db.delete(new_preference)
  await db.commit()
  return new_preference