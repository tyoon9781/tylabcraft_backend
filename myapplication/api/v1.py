from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from myapplication.database.crud import ItemCrud
from myapplication.database.schema import ItemSchema
from myapplication.database.connection import get_db

router = APIRouter()
prefix = "/api/v1"

@router.get("/")
async def health_check():
    return {"status" : "ok"}

@router.get("/items/{item_id}", response_model=ItemSchema.All)
async def read_item(item_id:int, db:Session=Depends(get_db)):
    return ItemCrud.read_item(item_id, db)

@router.get("/items", response_model=list[ItemSchema.All])
async def read_items(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    if not (isinstance(skip, int) and isinstance(limit, int) and skip >=0 and limit >= 0):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"invalid parameters. {skip=}, {limit=}")
    return ItemCrud.read_items(skip, limit, db)

@router.post("/items", response_model=ItemSchema.All)
async def create_item(item:ItemSchema.NeedCreate, db:Session=Depends(get_db)):
    return ItemCrud.create_item(item, db)

@router.put("/items/{item_id}", response_model=ItemSchema.All)
async def update_item(item_id:int, new_title:str, new_description:str, db:Session=Depends(get_db)):
    if len(new_title) == 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="new title is empty")
    return ItemCrud.update_item(item_id, new_title, new_description, db)

@router.delete("/items/{item_id}", response_model=ItemSchema.All)
async def delete_item(item_id:int, db:Session=Depends(get_db)):
    return ItemCrud.delete_item(item_id, db)
