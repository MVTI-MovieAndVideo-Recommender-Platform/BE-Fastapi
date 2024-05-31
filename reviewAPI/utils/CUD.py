from fastapi import HTTPException, Depends
from sqlalchemy import select
from model.models import StarORM,CreatedStar, UpdatedStar,DeletedStar, LikeORM, CreatedLike, DeletedLike
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db

async def create_star(cs:CreatedStar, db: AsyncSession = Depends(get_db)):
  new_star = StarORM(content_index = cs.content_index, user_id = cs.user_id, star = cs.star)
  db.add(new_star)
  await db.commit()
  await db.refresh(new_star) 
  return new_star

async def update_star(us:UpdatedStar, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(StarORM).where(StarORM.star_index == us.star_index))
  new_star = result.scalar_one_or_none()
  if new_star is None:
    raise HTTPException(status_code=404, detail="star not found")
  new_star.star = us.star
  await db.commit()
  return new_star

async def delete_star(ds:DeletedStar, db: AsyncSession = Depends(get_db)):
  # users 테이블에서 모든 행 선택
  result = await db.execute(select(StarORM).where(StarORM.star_index == ds.star_index))
  new_star = result.scalar_one_or_none()
  if new_star is None:
      raise HTTPException(status_code=404, detail="star not found")
  await db.delete(new_star)
  await db.commit()
  return new_star

async def create_like(cl:CreatedLike, db: AsyncSession = Depends(get_db)):
  new_star = LikeORM(content_index = cl.content_index, user_id = cl.user_id)
  db.add(new_star)
  await db.commit()
  await db.refresh(new_star) 
  return new_star

async def delete_like(dl:DeletedLike, db: AsyncSession = Depends(get_db)):
  # users 테이블에서 모든 행 선택
  result = await db.execute(select(LikeORM).where(LikeORM.like_index == dl.like_index))
  new_like = result.scalar_one_or_none()
  if new_like is None:
      raise HTTPException(status_code=404, detail="like not found")
  await db.delete(new_like)
  await db.commit()
  return new_like