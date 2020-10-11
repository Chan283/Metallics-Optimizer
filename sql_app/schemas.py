from typing import List
from pydantic import BaseModel


class ChemicalBase(BaseModel):
    pass

class ChemicalCreate(ChemicalBase):
    name: str
    percentage: int

class Chemical(ChemicalBase):
    id: int
    name: str
    percentage: int

    class Config:
        orm_mode = True


class CommodityBase(BaseModel):
    name: str


class CommodityCreate(CommodityBase):
    name: str
    inventory: float
    price: float


class Commodity(CommodityBase):
    id: int
    name: str
    inventory: float
    price: float
    chemicals: List[Chemical] = []

    class Config:
        orm_mode = True
