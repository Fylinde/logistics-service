from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseModel

class StockModel(BaseModel):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)
    product_id = Column(Integer, nullable=False)  # Referencing Product from Product-Service
    quantity = Column(Float, nullable=False)  # Quantity available in the warehouse
    stock = Column(Integer, nullable=False, default=0)  # Number of items available at this warehouse

    warehouse = relationship("WarehouseModel", back_populates="stocks")
