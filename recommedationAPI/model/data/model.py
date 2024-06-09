from pydantic import BaseModel
from typing import List


class content(BaseModel):
  index: int
  title: str
  genres: str 
  overview: str

class RecommenderInput(BaseModel):
  mbti: str 
  preference: List[str]