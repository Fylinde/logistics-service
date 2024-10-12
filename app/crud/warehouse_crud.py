from sqlalchemy.orm import Session
from app.models.warehouse import WarehouseModel
from app.schemas.warehouse_schemas import WarehouseCreate

def create_warehouse(db: Session, warehouse: WarehouseCreate):
    db_warehouse = WarehouseModel(**warehouse.dict())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse

def get_warehouse_by_id(db: Session, warehouse_id: int):
    return db.query(WarehouseModel).filter(WarehouseModel.id == warehouse_id).first()

def get_all_warehouses(db: Session):
    return db.query(WarehouseModel).all()

def update_warehouse(db: Session, warehouse_id: int, updated_warehouse: WarehouseCreate):
    db_warehouse = get_warehouse_by_id(db, warehouse_id)
    if db_warehouse:
        for key, value in updated_warehouse.dict().items():
            setattr(db_warehouse, key, value)
        db.commit()
        db.refresh(db_warehouse)
    return db_warehouse

def delete_warehouse(db: Session, warehouse_id: int):
    db_warehouse = get_warehouse_by_id(db, warehouse_id)
    if db_warehouse:
        db.delete(db_warehouse)
        db.commit()
    return db_warehouse

# Retrieve all warehouses
def get_all_warehouses(db: Session):
    return db.query(WarehouseModel).all()

