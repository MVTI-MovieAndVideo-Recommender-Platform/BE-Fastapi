# 라이브러리 
from typing import List
from fastapi import Query,HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

#변수, 함수
from config.database import DATABASE_NAME, MONGO_URI, COLLECTION_NAME
from models.models import Content

# MongoDB 연결 확인
async def check_db_connection():
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DATABASE_NAME]
        await db.command("ping")
        return True
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return False

# FastAPI Depends를 사용하여 MongoDB 연결 주입
async def get_database():
    if await check_db_connection():
        client = AsyncIOMotorClient(MONGO_URI)
        database = client.get_database(DATABASE_NAME)
        yield database
        client.close()
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")
    

# 유효한 형식인지 확인 
async def isValid(contents):
    result = []
    try:
        for content in contents:
            result.append(Content(**content))
    except ValidationError as e:
        print("Validation error for valid item:", e)
    return result


# 검색 
async def fetch_contents(database, search: str = Query(None), conditions:List[str] = Query(None), condition_fields:List[str]=Query(None)):
    condition_query = {}
    query_temp = []
    query = {}
    search_query = {
        "$or": [
            {"name": {"$regex": f".*{search}.*", "$options": "i"}},
            {"overview": {"$regex": f".*{search}.*", "$options": "i"}},
            {"country": {"$regex": f".*{search}.*", "$options": "i"}},
            {"genres": {"$regex": f".*{search}.*", "$options": "i"}},
            {"content_type": {"$regex": f".*{search}.*", "$options": "i"}}
        ]
    }
    print("conditions:",conditions)
    print("condition_fields:",condition_fields)
    if conditions and condition_fields:
        and_condition = []
        if len(conditions) == len(condition_fields):
            for i in range(0, len(condition_fields)):
                and_condition.append({str(condition_fields[i]):{"$regex":f".*{str(conditions[i])}*","$options":"i"}})
            condition_query["$and"]=and_condition
    
    query_temp.append(search_query)
    query_temp.append(condition_query)
    query["$and"] = query_temp
    print(query)
    contents = await db_query(database, query,100)
    
    return contents

# db에 접속해서 query 전달 후 조회 
async def db_query(database, query, len):
    collections = database.get_collection(COLLECTION_NAME)
    contents = await collections.find(query).to_list(length=len)
    contents = await isValid(contents)
    return contents