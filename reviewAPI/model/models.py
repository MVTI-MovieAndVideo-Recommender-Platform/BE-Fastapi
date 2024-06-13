from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class RatingORM(Base):
    __tablename__ = 'rating'
    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    media_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)

class PreferenceORM(Base):
    __tablename__ = 'preference'
    preference_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    media_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

# Pydantic model
class CreatedRating(BaseModel):
    media_id: int
    user_id: int
    rating: int

    class Config:
        orm_mode = True

class UpdatedRating(BaseModel):
    rating_id: int
    rating: int


class DeletedRating(BaseModel):
    rating_id: int
    
    class Config:
       orm_mode = True

class CreatedPreference(BaseModel):
    media_id: int
    user_id: int 

    class Config:
        orm_mode = True

class DeletedPreference(BaseModel):
    preference_id: int
    
    class Config:
       orm_mode = True