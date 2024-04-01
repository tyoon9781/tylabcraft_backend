from pydantic import BaseModel
from datetime import datetime

class ItemSchema:
    class NeedCreate(BaseModel):
        title: str
        description: str|None = None

    class All(BaseModel):
        id: int
        create_at: datetime
        title: str
        description: str|None = None
        