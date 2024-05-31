from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class StarORM(Base):
    __tablename__ = 'star'
    star_index = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content_index = Column(Integer, nullable=False)
    user_id = Column(String(length=255), nullable=False)
    star = Column(Integer, nullable=False)

class LikeORM(Base):
    __tablename__ = 'user_like'
    like_index = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content_index = Column(Integer, nullable=False)
    user_id = Column(String(length=255), nullable=False)

# Pydantic model
class CreatedStar(BaseModel):
    content_index: int
    user_id: str
    star: int

    class Config:
        orm_mode = True

class UpdatedStar(BaseModel):
    star_index: int
    star: int

    class Config:
        orm_mode = True

class DeletedStar(BaseModel):
    star_index: int
    
    class Config:
       orm_mode = True
# Pydantic model
class CreatedLike(BaseModel):
    content_index: int
    user_id: str 

    class Config:
        orm_mode = True

class DeletedLike(BaseModel):
    like_index: int
    
    class Config:
       orm_mode = True