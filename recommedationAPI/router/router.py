# app/routers/review.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from utils import embedding, recommender, cud
from model.model import content, RecommenderInput, delete_recommendation
from database.database import get_db


router = APIRouter()

# 추천 함수 
@router.post("/recommedation")
async def recommend_endpoint(ri:RecommenderInput, db: AsyncSession = Depends(get_db)):
    return await recommender.get_recommendations(ri, db)

@router.delete("/delete_recommend")
async def delete_recommend_endpoint(dr: delete_recommendation, db: AsyncSession = Depends(get_db)):
    return await cud.delete_recommendation(dr, db)

# 콘텐츠 데이터가 업로드 될 경우 임베딩 진행 
@router.post("/content_embedding")
async def content_embedding(contents:List[content]):
    return await embedding.embedding(contents) 