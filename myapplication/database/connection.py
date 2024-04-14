from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

## Environment Variables
load_dotenv()

## Construct a base class for declaractive class definitions
Base: DeclarativeBase = declarative_base()

class ConnectDB:
    is_test = False

    def init_db(self, is_test=None):
        if is_test is None:
            is_test = self.is_test
        _db_url = os.getenv("TEST_DB_URL") if is_test else os.getenv("DB_URL")
        _engine = create_engine(_db_url)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    def get_db(self):
        db = self.session()
        try:
            yield db
        finally:
            db.close()

connect_db = ConnectDB()