from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from typing import List, Optional, Union

Base = declarative_base()

class ContentORM(Base):
    __tablename__ = 'content'
    content_index = Column(Integer, primary_key=True, index=True, autoincrement=True)


# Pydantic model
class CreatedContent(BaseModel):
    index: int
    name: str 
    img_url: str 
    flatrate: Optional[str] = None 
    overview: Optional[str] = None  
    country: Optional[str] = None 
    age_rating: Optional[str] = None 
    year: Optional[int] = None  
    genres: Optional[str] = None  
    content_type: Optional[str] = None  

class UpdatedContent(BaseModel):
    content_index: int

class DeletedContent(BaseModel):
    content_index: int
    
    class Config:
       orm_mode = True