from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from model.models import MovieORM, SeriesORM, CreatedContent, ContentType, UpdatedContent, DeletedContent
from db_connection.database import get_db

async def create_content(cu:CreatedContent, db: AsyncSession = Depends(get_db)):
    if cu.content_type == ContentType.movie:
        # 영화 콘텐츠의 최대 인덱스를 조회하고 홀수 인덱스 생성
        result = await db.execute(select(func.max(MovieORM.content_index)))
        max_index = result.scalar() or 0
        new_index = max_index + 2 if max_index % 2 != 0 else max_index + 1
        new_content = MovieORM(content_index=new_index, **cu.dict(exclude={"content_type"}))
    elif cu.content_type == ContentType.series:
        # 시리즈 콘텐츠의 최대 인덱스를 조회하고 짝수 인덱스 생성
        result = await db.execute(select(func.max(SeriesORM.content_index)))
        max_index = result.scalar() or 0
        new_index = max_index + 2 if max_index % 2 == 0 else max_index + 1
        new_content = SeriesORM(content_index=new_index, **cu.dict(exclude={"content_type", "disp_rtm"}))
    else:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    db.add(new_content)
    await db.commit()
    await db.refresh(new_content)
    return new_content

async def update_content(uc: UpdatedContent, db: AsyncSession = Depends(get_db)):
    content_index = uc.content_index
    if content_index & 1:  # 홀수이면 Movie
        result = await db.execute(select(MovieORM).where(MovieORM.content_index == content_index))
    else:  # 짝수이면 Series
        result = await db.execute(select(SeriesORM).where(SeriesORM.content_index == content_index))

    db_content = result.scalar_one_or_none()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    for key, value in uc.dict(exclude_unset=True, exclude={"content_type"}).items():
        setattr(db_content, key, value)
    
    await db.commit()
    await db.refresh(db_content)
    db_content.content_type = ContentType.movie if content_index & 1 else ContentType.series  # content_type 설정
    return db_content

async def delete_content(dc: DeletedContent, db: AsyncSession = Depends(get_db)):
    content_index = dc.content_index
    if content_index & 1:
        result = await db.execute(select(MovieORM).where(MovieORM.content_index == dc.content_index))
    else:
        result = await db.execute(select(SeriesORM).where(SeriesORM.content_index == dc.content_index))
    
    db_content = result.scalar_one_or_none()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    await db.delete(db_content)
    await db.commit()
    return db_content
