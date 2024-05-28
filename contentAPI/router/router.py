# app/routers/content.py
from fastapi import APIRouter, Depends
from model.models import CreatedContent, UpdatedContent, DeletedContent, ResponseContent
from sqlalchemy.ext.asyncio import AsyncSession

from db_connection.database import get_db
from utils.CUD import create_content, update_content, delete_content

router = APIRouter()

@router.post("/create_content", response_model=ResponseContent)
async def content_create_endpoint(cr: CreatedContent, db: AsyncSession = Depends(get_db)):
    return await create_content(cr,db)

@router.put("/update_content", response_model=UpdatedContent)
async def update_content_endpoint(ur: UpdatedContent, db: AsyncSession = Depends(get_db)):
    return await update_content(ur,db)

@router.delete("/delete_content", response_model= DeletedContent)
async def delete_content_endpoint(dr:DeletedContent, db: AsyncSession = Depends(get_db)):
    return await delete_content(dr, db)
