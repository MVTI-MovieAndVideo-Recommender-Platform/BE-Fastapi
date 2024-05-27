from fastapi import FastAPI
from config.cors import setup_cors
from router import router

app = FastAPI()

setup_cors(app)

app.include_router(router.router, prefix="/reviews")