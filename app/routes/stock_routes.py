from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.stock import StockCreate, StockUpdate, Stock
from app.crud.stock_crud import (
    add_stock, 
    update_stock, 
    remove_stock, 
    get_stock_for_product, 
    get_total_stock_for_product
)
from app.utils.rabbitmq import RabbitMQConnection


router = APIRouter()

# Add stock to a warehouse for a product
@router.post("/", response_model=Stock, status_code=status.HTTP_201_CREATED)
def add_stock_route(stock: StockCreate, db: Session = Depends(get_db)):
    db_stock = add_stock(db, stock)
    return db_stock

# Update stock in a specific warehouse for a product
@router.put("/{product_id}/{warehouse_id}", response_model=Stock, status_code=status.HTTP_200_OK)
def update_stock_route(product_id: int, warehouse_id: int, new_quantity: int, db: Session = Depends(get_db)):
    # Update the stock in the database
    updated_stock = update_stock(db, product_id, warehouse_id, new_quantity)

    # Publish the stock update event to RabbitMQ
    rabbitmq = RabbitMQConnection(queue_name='stock_queue')
    message = {
        "event": "stock_updated",
        "product_id": product_id,
        "warehouse_id": warehouse_id,
        "new_quantity": new_quantity,
    }
    rabbitmq.publish_message(message)
    rabbitmq.close_connection()

    return updated_stock


# Remove stock for a product from a specific warehouse
@router.delete("/{product_id}/{warehouse_id}", status_code=status.HTTP_200_OK)
def remove_stock_route(product_id: int, warehouse_id: int, db: Session = Depends(get_db)):
    removed = remove_stock(db, product_id, warehouse_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"detail": "Stock removed"}

# Get stock information for a product across all warehouses
@router.get("/{product_id}", response_model=List[Stock], status_code=status.HTTP_200_OK)
def get_stock_for_product_route(product_id: int, db: Session = Depends(get_db)):
    stock_info = get_stock_for_product(db, product_id)
    return stock_info

# Get the total stock for a product across all warehouses
@router.get("/{product_id}/total", response_model=int, status_code=status.HTTP_200_OK)
def get_total_stock_for_product_route(product_id: int, db: Session = Depends(get_db)):
    total_stock = get_total_stock_for_product(db, product_id)
    return total_stock
