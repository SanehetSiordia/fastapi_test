from sqlmodel import SQLmodel, Field

class ItemBase(SQLmodel):
    name: str=Field()
    price: float=Field()
    stock: int=Field()

class ItemCreateIn(ItemBase):

class itemCreateOut(SQLmodel):
    id: int=Field()

class Item(ItemBase, table=true):
    id: int=Field(primary_key=True)