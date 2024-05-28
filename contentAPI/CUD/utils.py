from fastapi import HTTPException

from sqlalchemy import select
from models import ContentORM,CreatedContent, UpdatedContent,DeletedContent
from database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def create_content(db: AsyncSession, cr:CreatedContent):
    # 커스텀 AUTO_INCREMENT 증가 값 관리
    result = await db.execute(select(cr.index).order_by(cr.index.desc()).limit(1))
    last_id = result.scalar()
    next_id = 2 if last_id is None else last_id + 2

    db_review = CreatedContent(
        index=next_id,
        name=cr.name,
        img_url=cr.img_url,
        flatrate=cr.flatrate,
        overview=cr.overview,
        country=cr.country,
        age_rating=cr.age_rating,
        year=cr.year,
        genres=cr.genres,
        content_type=cr.content_type
    )
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def update_content(ur:UpdatedContent):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ContentORM).where(ContentORM.content_index == ur.content_index))
        new_content = result.scalar_one_or_none()
        if new_content is None:
          raise HTTPException(status_code=404, detail="content not found")
        new_content.content = ur.content
        await session.commit()
        return new_content
    
async def delete_content(dr:DeletedContent):
    async with AsyncSessionLocal() as session:
        # users 테이블에서 모든 행 선택
        result = await session.execute(select(ContentORM).where(ContentORM.content_index == dr.content_index))
        new_content = result.scalar_one_or_none()
        if new_content is None:
            raise HTTPException(status_code=404, detail="content not found")
        await session.delete(new_content)
        await session.commit()
        return new_content