from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from .connection import Base


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, default=datetime.now)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=True)