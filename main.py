# 라이브러리 
from typing import List

from fastapi import FastAPI,Depends ,Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

#변수, 함수
from models.models import Content
from api.search_api import fetch_contents, db_query, get_database, isValid

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

# FastAPI 엔드포인트
@app.get("/search/", response_model=List[Content])
async def read_contents(database = Depends(get_database), search:str = Query(None), conditions:List[str] = Query(None),condition_fields: List[str] = Query(None)):
    contents = await fetch_contents(database, search, conditions, condition_fields)
    return contents


# 상세 페이지 정보 넘기기, index를 통해 접속 
@app.get("/index/{index}", response_model=Content)
async def content_info(index,database = Depends(get_database)):
    content = await db_query(database, {"index":int(index)},1)
    return content[0]

# 서버 실행 코드 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

