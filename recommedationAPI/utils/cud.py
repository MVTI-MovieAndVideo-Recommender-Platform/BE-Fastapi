from fastapi import HTTPException, Depends
from model.model import delete_recommendation, RecommendORM, RecommenderInput
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_db
from datetime import datetime


async def create_recommendation(ri: RecommenderInput, result, re_recommendation,db):
  new_recommend = RecommendORM(user_id = ri.user_id, mbti = ri.mbti, preference = ri.preference, recommendation_results = result, last_update = datetime.now(), re_recommendation = re_recommendation)
  db.add(new_recommend)
  await db.commit()
  await db.refresh(new_recommend) 
  return new_recommend

async def delete_recommendation(dr: delete_recommendation, db):
  result = await db.execute(select(RecommendORM).where(RecommendORM.recommend_id == dr.recommend_id))
  new_recommend = result.scalar_one_or_none()
  if new_recommend is None:
      raise HTTPException(status_code=404, detail="recommendation not found")
  await db.delete(new_recommend)
  await db.commit()
  return new_recommend