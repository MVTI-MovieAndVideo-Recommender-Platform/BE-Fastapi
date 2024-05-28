# app/routers/review.py
from fastapi import APIRouter, Depends
from model.models import CreatedReview, UpdatedReview, DeletedReview
from sqlalchemy.ext.asyncio import AsyncSession

from db_connection.database import get_db
from utils.CUD import create_review, update_review, delete_review

router = APIRouter()

@router.post("/review_create", response_model=CreatedReview)
async def review_create_endpoint(cr: CreatedReview, db: AsyncSession = Depends(get_db)):
    return await create_review(cr,db)

@router.put("/review_update", response_model=UpdatedReview)
async def update_review_endpoint(ur: UpdatedReview, db: AsyncSession = Depends(get_db)):
    return await update_review(ur,db)

@router.delete("/review_delete", response_model= DeletedReview)
async def delete_review_endpoint(dr:DeletedReview, db: AsyncSession = Depends(get_db)):
    return await delete_review(dr, db)
