from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class ReviewORM(Base):
    __tablename__ = 'review'
    review_index = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content_index = Column(Integer, nullable=False)
    user_id = Column(String(length=255), nullable=False)
    review = Column(Boolean, nullable=False)

# Pydantic model
class CreatedReview(BaseModel):
    content_index: int
    user_id: str
    review: bool

    class Config:
        orm_mode = True

class UpdatedReview(BaseModel):
    review_index: int
    review: int

    class Config:
        orm_mode = True

class DeletedReview(BaseModel):
    review_index: int
    
    class Config:
       orm_mode = True