from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .connection import Base


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, default=datetime.now)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    # is_active = Column(Boolean, nullable=True, server_default='true')