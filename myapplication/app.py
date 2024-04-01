from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from myapplication.api import v1
from myapplication.database.connection import init_db

from dotenv import load_dotenv
import os

## environment variable
load_dotenv()

## Initialize DB
init_db()

## Init Web Application Instanceo
origins = [
    f"{os.getenv('BACKEND_HOST')}",     ## backend ip
    "http://localhost:3000",            ## next.js test
    "http://tylabcraft.com",            ## main url
]
    
app_instance = FastAPI()
app_instance.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, ## cookie allow
    allow_methods=["*"],
    allow_headers=["*"],
)
app_instance.include_router(v1.router, prefix=v1.prefix)

@app_instance.get('/')
async def healthcheck():
    return {"status": "ok"}
