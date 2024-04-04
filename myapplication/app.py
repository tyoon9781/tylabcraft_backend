from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from myapplication.api import v1
from myapplication.database.connection import connect_db
from dotenv import load_dotenv

import os

## Initialize DB
load_dotenv()
connect_db.init_db()

## Init Web Application Instanceo
allow_origins = os.getenv('ALLOW_ORIGINS').split(",")
    
app_instance = FastAPI()
app_instance.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True, ## cookie allow
    allow_methods=["*"],
    allow_headers=["*"],
)
app_instance.include_router(v1.router, prefix=v1.prefix)

@app_instance.get('/')
async def healthcheck():
    return {"status": "ok"}
