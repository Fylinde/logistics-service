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
    vendor_id: int  # Linking the warehouse to a vendor

    class Config:
        orm_mode = True


class WarehouseResponse(WarehouseCreate):
    id: int


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class Warehouse(WarehouseBase):
    id: int
    vendor_id: int

    class Config:
        orm_mode = True