# app/routers/review.py
from fastapi import APIRouter, Depends
from model.models import CreatedRating, CreatedPreference, UpdatedRating, DeletedPreference, DeletedRating
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from utils.CUD import create_rating, delete_rating,update_rating ,create_preference, delete_preference

router = APIRouter()

@router.post("/rating_create", response_model=CreatedRating)
async def create_rating_endpoint(cs: CreatedRating, db: AsyncSession = Depends(get_db)):
    return await create_rating(cs,db)

@router.put("/rating_update", response_model=UpdatedRating)
async def update_rating_endpoint(us: UpdatedRating, db: AsyncSession = Depends(get_db)):
    return await update_rating(us,db)

@router.delete("/rating_delete", response_model= DeletedRating)
async def delete_rating_endpoint(ds:DeletedRating, db: AsyncSession = Depends(get_db)):
    return await delete_rating(ds, db)

@router.post("/preference_create", response_model=CreatedPreference)
async def create_preference_endpoint(cl:CreatedPreference , db: AsyncSession = Depends(get_db)):
    return await create_preference(cl,db)

@router.delete("/preference_delete", response_model= DeletedPreference)
async def delete_preference_endpoint(dl: DeletedPreference, db: AsyncSession = Depends(get_db)):
    return await delete_preference(dl, db)

