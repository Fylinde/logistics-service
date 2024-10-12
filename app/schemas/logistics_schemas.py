from pydantic import BaseModel

class ShipmentRouteRequest(BaseModel):
    buyer_location: str
    seller_id: int

    class Config:
        orm_mode = True
