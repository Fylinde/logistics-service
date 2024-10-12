from sqlalchemy.orm import Session
from app.models.warehouse import WarehouseModel
from app.crud.warehouse_crud import get_all_warehouses
from app.utils.logistics_utils import calculate_proximity
from app.utils.email import send_email
from app.config import settings
from app.services.product_service_client import get_product_stock, update_product_stock_in_product_service

def find_nearest_warehouse(db: Session, buyer_location: str):
    """
    Find the nearest warehouse to the buyer's location based on proximity.
    
    :param db: Database session
    :param buyer_location: The buyer's coordinates (latitude,longitude)
    :return: The nearest warehouse
    """
    warehouses = get_all_warehouses(db)
    nearest_warehouse = None
    min_distance = float('inf')

    for warehouse in warehouses:
        distance = calculate_proximity(buyer_location, warehouse.location)
        if distance < min_distance:
            min_distance = distance
            nearest_warehouse = warehouse

    return nearest_warehouse



def add_new_product_to_warehouse(db_session, product_id, product_name, initial_stock):
    """
    Add a new product to the nearest warehouse or a specific warehouse.
    """
    # You can implement logic here to assign the product to the nearest warehouse or multiple warehouses
    # For example, you could distribute the initial stock to multiple warehouses based on the logic
    warehouse = find_nearest_warehouse(db_session, 'default_location')  # For example, you can replace 'default_location' with actual logic
    if warehouse:
        # Add the product to the warehouse (pseudo code for illustration)
        warehouse.add_product(product_id, product_name, initial_stock)
        db_session.commit()
    else:
        print("No warehouse found to add the product")

def update_warehouse_stock(db_session, product_id, warehouse_id, new_quantity):
    """
    Update stock for a given product in a specific warehouse by delegating to Product-Service.
    """
    print(f"Delegating stock update for Product {product_id} in Warehouse {warehouse_id} to Product-Service")

    # Call the Product-Service to update the stock
    success = update_product_stock_in_product_service(product_id, warehouse_id, new_quantity)
    
    if success:
        print(f"Successfully updated stock for Product {product_id} in Warehouse {warehouse_id} via Product-Service")
    else:
        print(f"Failed to update stock for Product {product_id} in Warehouse {warehouse_id} via Product-Service")

# app/services/logistics_service.py

def update_inventory_after_shipment(db_session, product_id, warehouse_id, quantity_shipped):
    """
    Update stock after an order is shipped, querying Product-Service for stock.
    """
    stock_data = get_product_stock(product_id, warehouse_id)
    if stock_data:
        current_stock = stock_data['stock']
        new_stock = max(0, current_stock - quantity_shipped)
        print(f"Updating stock for Product {product_id}: {current_stock} -> {new_stock}")
        # Optionally send a stock update event via RabbitMQ to Product-Service if needed
    else:
        print(f"Failed to update stock for Product {product_id} in Warehouse {warehouse_id} due to missing data.")
        
        
def notify_stock_low(db_session, product_id, warehouse_id, remaining_stock):
    """
    Notify the logistics team when stock is running low.
    This function sends an email notification and could trigger other actions like stock replenishment.
    """
    print(f"Stock is low for Product {product_id} in Warehouse {warehouse_id}. Remaining stock: {remaining_stock}")

    # Send email notification to logistics team
    subject = f"Low Stock Alert: Product {product_id} in Warehouse {warehouse_id}"
    body = (f"Attention!\n\n"
            f"Stock for Product {product_id} in Warehouse {warehouse_id} is running low.\n"
            f"Remaining stock: {remaining_stock} units.\n\n"
            f"Please take necessary actions to replenish the stock.\n"
            f"Thank you!")
    
    # You can use the team email from the settings or hardcode it
    team_email = settings.LOGISTICS_TEAM_EMAIL

    # Send the email using the email utility function
    send_email(team_email, subject, body)

    # Example: If stock is below a critical threshold, trigger replenishment
    CRITICAL_STOCK_THRESHOLD = 10
    if remaining_stock < CRITICAL_STOCK_THRESHOLD:
        print(f"Stock for Product {product_id} in Warehouse {warehouse_id} is critically low! Initiating replenishment process.")
        initiate_replenishment(db_session, product_id, warehouse_id, CRITICAL_STOCK_THRESHOLD)

def initiate_replenishment(db_session, product_id, warehouse_id, replenish_quantity):
    """
    Initiate the replenishment process for the given product and warehouse.
    This could involve creating a purchase order, notifying the supplier, or updating the procurement system.
    """
    # Example logic to initiate a stock replenishment
    print(f"Initiating replenishment for Product {product_id} in Warehouse {warehouse_id}. Replenishing stock to {replenish_quantity} units.")

    # You could also insert a new replenishment order in the database, call a supplier API, etc.
    # Example:
    # supplier_order = create_supplier_order(product_id, warehouse_id, replenish_quantity)
    # db_session.add(supplier_order)
    # db_session.commit()

    # For now, we'll just simulate this with a print statement
    print(f"Replenishment process initiated for Product {product_id} in Warehouse {warehouse_id}.")
