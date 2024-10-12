from pydantic import BaseModel
from typing import Optional


class StockBase(BaseModel):
    product_id: int
    warehouse_id: int
    stock: int  # Number of units in stock


class StockCreate(BaseModel):
    warehouse_id: int
    product_id: int
    quantity: float

    class Config:
        orm_mode = True

class Stock(StockBase):
    id: int  # Stock ID for the record

    class Config:
        orm_mode = True


class StockUpdate(BaseModel):
    stock: Optional[int] = None  # Allow partial update of stock
            
class StockResponse(StockCreate):
    id: int

class ProductStockSummary(BaseModel):
    """
    Schema to display the summary of stock across all warehouses for a product.
    """
    product_id: int
    total_stock: int
    stock_details: list  # Holds a list of warehouse stocks with details

    class Config:
        orm_mode = True