from typing import List, Optional, Union
from pydantic import BaseModel

class series(BaseModel):
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


class movie(BaseModel):
    index: int
    name: str 
    img_url: str 
    flatrate: Optional[str] = None 
    overview: Optional[str] = None 
    disp_rtm: Optional[str] = None 
    age_rating: Optional[str] = None  
    year: Optional[int] = None  
    genres: Optional[str] = None  
    country: Optional[str] = None 

class recommanded_log(BaseModel):
    recommanded_index: int
    
class search_log(BaseModel):
    recommanded_index: int

class detail_log(BaseModel):
    recommanded_index: int

class user(BaseModel):
    user_id: str


