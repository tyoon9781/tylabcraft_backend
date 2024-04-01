from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

## Environment Variable
DB_TYPE = os.getenv("DB_TYPE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_TEST = os.getenv("DB_TEST")
IS_TEST = os.getenv("IS_TEST", "FALSE")

if None in [DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_TEST]:
    print(f"{DB_TYPE=}, {DB_USER=}, {DB_PASSWORD=}, {DB_HOST=}, {DB_PORT=}, {DB_NAME=}, {DB_TEST=}")
    raise ValueError("Some database environment variables are missing")

## Construct a base class for declaractive class definitions
Base = declarative_base()

## Database Session
_db_name = DB_TEST if IS_TEST == "TRUE" else DB_NAME
_db_connection = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{_db_name}"
_engine = create_engine(_db_connection)
_session = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def init_db():
    Base.metadata.create_all(bind=_engine)


def get_db():
    db = _session()
    try:
        yield db
    finally:
        db.close()
