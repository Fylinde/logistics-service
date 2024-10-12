from sqlalchemy.orm import Session
from app.models.stock import StockModel
from app.schemas.stock_schemas import StockCreate

def add_stock(db: Session, stock: StockCreate):
    db_stock = StockModel(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stock_by_warehouse(db: Session, warehouse_id: int):
    return db.query(StockModel).filter(StockModel.warehouse_id == warehouse_id).all()

# Update stock in a specific warehouse
def update_stock(db: Session, product_id: int, warehouse_id: int, new_quantity: int):
    db_stock = db.query(ProductStockModel).filter(
        ProductStockModel.product_id == product_id,
        ProductStockModel.warehouse_id == warehouse_id
    ).first()
    
    if db_stock:
        db_stock.stock = new_quantity
        db.commit()
        db.refresh(db_stock)
        return db_stock
    return None

# Remove stock from a specific warehouse
def remove_stock(db: Session, product_id: int, warehouse_id: int):
    db_stock = db.query(ProductStockModel).filter(
        ProductStockModel.product_id == product_id,
        ProductStockModel.warehouse_id == warehouse_id
    ).first()
    
    if db_stock:
        db.delete(db_stock)
        db.commit()
        return True
    return False

# Get stock for a product across all warehouses
def get_stock_for_product(db: Session, product_id: int):
    return db.query(ProductStockModel).filter(ProductStockModel.product_id == product_id).all()

# Get total stock for a product across all warehouses
def get_total_stock_for_product(db: Session, product_id: int):
    stock_records = db.query(ProductStockModel).filter(ProductStockModel.product_id == product_id).all()
    total_stock = sum([stock.stock for stock in stock_records])
    return total_stock
