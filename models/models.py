from typing import List, Optional, Union
from pydantic import BaseModel

class Content(BaseModel):
    index: int
    name: str 
    img_url: str 
    flatrate: str 
    overview: Optional[str] = None  # 선택적 필드로 설정
    country: Optional[str] = None  # 선택적 필드로 설정
    age_rating: Optional[str] = None  # 선택적 필드로 설정
    year: Optional[int] = None  # 선택적 필드로 설정
    genres: Optional[str] = None  # 선택적 필드로 설정
    content_type: Optional[str] = None  # 선택적 필드로 설정

