# app/routers/review.py
from fastapi import APIRouter, Depends
from utils import embedding, recommender
from model.data.model import content, RecommenderInput

from typing import List

router = APIRouter()

# 추천 함수 
@router.post("/recommedation")
async def recommend_endpoint(ri:RecommenderInput):
    return await recommender.recommendation(ri)

# 콘텐츠 데이터가 업로드 될 경우 임베딩 진행 
@router.post("/content_embedding")
async def content_embedding(contents:List[content]):
    return await embedding.embedding(contents) 