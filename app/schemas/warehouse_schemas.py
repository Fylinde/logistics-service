from pydantic import BaseModel
from typing import Optional


class WarehouseBase(BaseModel):
    name: str
    location: str  # Location is important for routing orders
    
class WarehouseCreate(BaseModel):
    name: str
    location: str
    capacity: float
    available_space: float
    seller_id: int  # Linking the warehouse to a seller

    class Config:
        orm_mode = True


class WarehouseResponse(WarehouseCreate):
    id: int


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class Warehouse(WarehouseBase):
    id: int
    seller_id: int

    class Config:
        orm_mode = True