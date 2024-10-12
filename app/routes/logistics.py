from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.crud.warehouse_crud import create_warehouse, get_warehouse_by_id, get_all_warehouses
from app.crud.stock_crud import add_stock, get_stock_by_warehouse, update_stock, delete_stock
from app.schemas.warehouse_schemas import WarehouseCreate, WarehouseResponse
from app.schemas.stock_schemas import StockCreate
from app.database import get_db
from app.services.logistics_service import find_nearest_warehouse
from app.schemas.logistics_schemas import ShipmentRouteRequest

router = APIRouter()

# Warehouse Routes
@router.post("/warehouse/", response_model=WarehouseResponse, tags=["Logistics"])
def create_new_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    return create_warehouse(db, warehouse)

@router.get("/warehouse/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = get_warehouse_by_id(db, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

@router.get("/warehouses/", response_model=list[WarehouseResponse])
def get_warehouses(db: Session = Depends(get_db)):
    return get_all_warehouses(db)

# Stock Routes
@router.post("/stock/", response_model=StockCreate)
def add_stock_to_warehouse(stock: StockCreate, db: Session = Depends(get_db)):
    return add_stock(db, stock)

@router.get("/warehouse/{warehouse_id}/stock/", response_model=list[StockCreate])
def get_warehouse_stock(warehouse_id: int, db: Session = Depends(get_db)):
    return get_stock_by_warehouse(db, warehouse_id)

@router.put("/stock/{stock_id}", response_model=StockCreate)
def update_warehouse_stock(stock_id: int, quantity: float, db: Session = Depends(get_db)):
    """
    Update the stock quantity in a specific warehouse.
    
    :param stock_id: The ID of the stock record to update.
    :param quantity: The new quantity of stock available.
    :param db: Database session.
    :return: The updated stock record.
    """
    stock = update_stock(db, stock_id, quantity)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.delete("/stock/{stock_id}", response_model=StockCreate)
def delete_warehouse_stock(stock_id: int, db: Session = Depends(get_db)):
    """
    Delete a stock record from a specific warehouse.
    
    :param stock_id: The ID of the stock record to delete.
    :param db: Database session.
    :return: The deleted stock record.
    """
    stock = delete_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


# Real-time Stock Synchronization
def synchronize_stock(warehouse_id: int):
    """
    Placeholder function to synchronize stock across warehouses.
    In a real-world scenario, this might involve querying other warehouses
    or an external service to update stock levels.
    
    :param warehouse_id: The ID of the warehouse where stock is being updated.
    """
    print(f"Synchronizing stock for warehouse ID {warehouse_id}")


# Real-time Stock Synchronization
@router.put("/stock/{stock_id}/sync", response_model=StockCreate)
def sync_stock(stock_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Sync stock levels across all warehouses.
    
    :param stock_id: The ID of the stock record to sync.
    :param background_tasks: Background task manager to handle real-time sync.
    :param db: Database session.
    :return: The updated stock record.
    """
    stock = update_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    synchronize_stock(stock.warehouse_id, background_tasks)
    return stock

# Logistics Routes
@router.post("/logistics/nearest-warehouse")
def find_nearest_warehouse_route(buyer_location: str, db: Session = Depends(get_db)):
    nearest_warehouse = find_nearest_warehouse(db, buyer_location)
    if not nearest_warehouse:
        raise HTTPException(status_code=404, detail="No nearby warehouse found")
    return nearest_warehouse

@router.post("/logistics/shipment-route/")
def get_shipment_route(request: ShipmentRouteRequest, db: Session = Depends(get_db)):
    """
    API route to find available shipment routes for a seller to a given buyer's location.
    
    :param request: A request body containing buyer location and seller ID.
    :param db: Database session.
    :return: The optimal shipment route based on 3PL integrations and warehouse availability.
    """
    # Extract values from the request object and pass them to the function
    route = calculate_shipment_route(db, request.buyer_location, request.seller_id)
    
    if not route:
        raise HTTPException(status_code=404, detail="No shipping route available")
    
    return route

def calculate_shipment_route(db: Session, buyer_location: str, seller_id: int):
    """
    Placeholder function to calculate the optimal shipment route.
    In a real-world scenario, this would interact with 3PL providers or a shipping API.
    
    :param db: The database session for accessing warehouse and stock data.
    :param buyer_location: The location of the buyer.
    :param seller_id: The ID of the seller.
    :return: A mock route or some shipment-related information.
    """
    # Simulate finding the best route based on buyer location and stock availability
    return {
        "route": "Mock Route",
        "estimated_delivery_time": "3-5 days",
        "carrier": "3PL Provider Name",
        "warehouse_id": 1,  # Placeholder for the selected warehouse
    }
