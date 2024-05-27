from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.config import settings
from contextlib import asynccontextmanager

# 비동기 엔진 생성 
engine = create_async_engine( settings.DATABASE_URL, echo=True)

# 비동기 세션 생성
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session