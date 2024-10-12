from sqlalchemy import Column, Integer, String, Float
from app.database import BaseModel
from sqlalchemy.orm import relationship
class WarehouseModel(BaseModel):
    __tablename__ = 'warehouses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)  # Store lat, long coordinates as a string
    capacity = Column(Float, nullable=False)   # Total capacity of the warehouse
    available_space = Column(Float, nullable=False)  # Remaining space in the warehouse
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    
    
    stocks = relationship("ProductStockModel", back_populates="warehouse")
