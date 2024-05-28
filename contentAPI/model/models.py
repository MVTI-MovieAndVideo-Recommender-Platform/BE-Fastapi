from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from typing import List, Optional
from enum import Enum


Base = declarative_base()

class ContentType(str, Enum):
    series = "series"
    movie = "movie"

# 공통 필드를 포함하는 베이스 클래스
class ContentBase(Base):
    __abstract__ = True
    content_index = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(length=255), nullable=False)
    img_url = Column(String(length=255), nullable=False)
    flatrate = Column(String(length=255), nullable=False)
    overview = Column(String(length=2000), nullable=False)
    country = Column(String(length=255), nullable=False)
    age_rating = Column(String(length=255), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String(length=255), nullable=False)  # 변경된 부분

# 시리즈 모델
class SeriesORM(ContentBase):
    __tablename__ = 'series'

# 영화 모델
class MovieORM(ContentBase):
    __tablename__ = 'movie'
    disp_rtm = Column(String(length=255), nullable=True)


# Pydantic model
class CreatedContent(BaseModel):
    content_type: ContentType
    title: str
    img_url: str
    flatrate: str
    overview: str
    country: str
    disp_rtm: Optional[str]
    age_rating: str
    year: int
    genre: str

    class Config:
        orm_mode = True

class UpdatedContent(BaseModel):
    content_index: int
    title: Optional[str]
    img_url: Optional[str]
    flatrate: Optional[str]
    overview: Optional[str]
    country: Optional[str]
    disp_rtm: Optional[str]
    age_rating: Optional[str]
    year: Optional[int]
    genre: Optional[str]

    class Config:
        orm_mode = True

class DeletedContent(BaseModel):
    content_index: int
    
    class Config:
       orm_mode = True

class ResponseContent(BaseModel):
    title: str
    img_url: str
    flatrate: str
    overview: str
    country: str
    disp_rtm: Optional[str]
    age_rating: str
    year: int
    genre: str

    class Config:
        orm_mode = True