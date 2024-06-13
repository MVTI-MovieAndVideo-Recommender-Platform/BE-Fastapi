from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime

Base = declarative_base()

class RecommendORM(Base):
    __tablename__ = 'recommendations'
    recommend_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable = False)
    mbti = Column(String, nullable=False)
    preference = Column(JSON, nullable=False)
    recommendation_results = Column(JSON, nullable=False)
    last_update = Column(DateTime, default=datetime.now, nullable=False)
    re_recommendation = Column(Boolean, default=False, nullable=False)

class content(BaseModel):
  index: int
  title: str
  genres: str 
  overview: str

class RecommenderInput(BaseModel):
  user_id: int
  mbti: str 
  preference: List[str]
  previous_recommendations: Optional[List[str]] = None

 
class delete_recommendation(BaseModel):
  recommend_id: int 
 
  class Config:
    orm_mode = True
