from sqlmodel import SQLModel, Field
from typing import Optional

class ItemBase(SQLModel):
    name: str=Field()
    price: float=Field()
    stock: int=Field()

class ItemCreateIn(ItemBase): ...


class itemCreateOut(SQLModel):
    id: int=Field()

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)