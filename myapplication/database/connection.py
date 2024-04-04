from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
import os

## Construct a base class for declaractive class definitions
Base: DeclarativeBase = declarative_base()

class ConnectDB:
    is_test = False

    def init_db(self):
        ## Database Environment Variable
        DB_TYPE = os.getenv("DB_TYPE")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        DB_TEST = os.getenv("DB_TEST")

        if None in [DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_TEST]:
            raise ValueError("Some Database Environment variables are missing")

        ## Database Session
        _db_name = DB_TEST if self.is_test else DB_NAME
        _db_connection = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{_db_name}"
        _engine = create_engine(_db_connection)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

        Base.metadata.create_all(bind=_engine)

    def get_db(self):
        db = self.session()
        try:
            yield db
        finally:
            db.close()

connect_db = ConnectDB()