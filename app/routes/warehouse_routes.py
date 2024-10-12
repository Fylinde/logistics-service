from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
from app.crud.warehouse_crud import (
    create_warehouse, 
    get_warehouse_by_id, 
    update_warehouse, 
    delete_warehouse, 
    get_all_warehouses
)

router = APIRouter()

# Create a new warehouse
@router.post("/", response_model=Warehouse, status_code=status.HTTP_201_CREATED)
def create_warehouse_route(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = create_warehouse(db, warehouse)
    return db_warehouse

# Get a warehouse by its ID
@router.get("/{warehouse_id}", response_model=Warehouse, status_code=status.HTTP_200_OK)
def get_warehouse_by_id_route(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = get_warehouse_by_id(db, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

# Update a warehouse's details
@router.put("/{warehouse_id}", response_model=Warehouse, status_code=status.HTTP_200_OK)
def update_warehouse_route(warehouse_id: int, warehouse: WarehouseUpdate, db: Session = Depends(get_db)):
    updated_warehouse = update_warehouse(db, warehouse_id, warehouse)
    if not updated_warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return updated_warehouse

# Delete a warehouse
@router.delete("/{warehouse_id}", status_code=status.HTTP_200_OK)
def delete_warehouse_route(warehouse_id: int, db: Session = Depends(get_db)):
    deleted = delete_warehouse(db, warehouse_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return {"detail": "Warehouse deleted"}

# List all warehouses
@router.get("/", response_model=List[Warehouse], status_code=status.HTTP_200_OK)
def get_all_warehouses_route(db: Session = Depends(get_db)):
    warehouses = get_all_warehouses(db)
    return warehouses
