from typing import List, Optional, Union
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps

from pydantic import BaseModel

class content_series(BaseModel):
    index:int
    name: str
    star_avg: float
    img_url:str 
    flatrate: str 
    overview: str 
    country: str 
    age_rating: str
    year: int 
    genres: str  

# 연결 변수 
database_name = "content"
collection_name_series = "series"
MONGO_URI = "mongodb://localhost:27017"

# MongoDB 연결 설정
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database(database_name)
collection_seriese = db.get_collection(collection_name_series)

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        # MongoDB 연결을 시작할 때 실행될 작업들
        await client.server_info()  # MongoDB에 연결되었는지 확인하는 간단한 명령
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    yield
    client.close()

app = FastAPI()

# CORS 설정 
origins = [
	"*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search/{hi}")
async def read_root(hi):
    return hi


# 상세 페이지 정보 넘기기, index를 통해 접속 
@app.get("/detail/{index}")
async def detail_info(index):
    item = await collection_seriese.find_one({"index":int(index)})
    # ObjectId 필드를 직렬화하여 JSON으로 변환
    item["_id"] = str(item["_id"])
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


