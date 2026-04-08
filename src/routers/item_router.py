from fastapi import APIRouter
from src.models.items import Item, ItemCreateIn, itemCreateOut
from src.config.database import SessionDep
from sqlmodel import Session, select

items_router = APIRouter(prefix="/items", tags=["Item"])

@items_router.get("/", response_model=list[Item])
def get_items(db: SessionDep):
    statement = select(Item)
    return db.exec(statement).all()

@items_router.post("/", response_model=itemCreateOut)
def add_item(item: ItemCreateIn, db: SessionDep):
    db_item = Item.model_validate(item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
