# app/routers/review.py
from fastapi import APIRouter, Depends
from model.models import CreatedStar, CreatedLike, UpdatedStar, DeletedLike, DeletedStar
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from utils.CUD import create_star, update_star, delete_star, create_like, delete_like

router = APIRouter()

@router.post("/star_create", response_model=CreatedStar)
async def create_star_endpoint(cs: CreatedStar, db: AsyncSession = Depends(get_db)):
    return await create_star(cs,db)

@router.put("/star_update", response_model=UpdatedStar)
async def update_star_endpoint(us: UpdatedStar, db: AsyncSession = Depends(get_db)):
    return await update_star(us,db)

@router.delete("/star_delete", response_model= DeletedStar)
async def delete_star_endpoint(ds:DeletedStar, db: AsyncSession = Depends(get_db)):
    return await delete_star(ds, db)

@router.post("/like_create", response_model=CreatedLike)
async def create_like_endpoint(cl:CreatedLike , db: AsyncSession = Depends(get_db)):
    return await create_like(cl,db)

@router.delete("/like_delete", response_model= DeletedLike)
async def delete_like_endpoint(dl: DeletedLike, db: AsyncSession = Depends(get_db)):
    return await delete_like(dl, db)

