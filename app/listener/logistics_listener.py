import pika
import json
from app.database import SessionLocal  # Import the session creator from your database config
from app.services.logistics_service import (
    find_nearest_warehouse,
    update_warehouse_stock,
    add_new_product_to_warehouse,
    update_inventory_after_shipment,
    notify_stock_low
)

# Function to handle the 'OrderCreated' event
def on_order_created(ch, method, properties, body):
    print("Received order created event")
    order_data = json.loads(body)
    buyer_location = order_data.get('buyer_location')

    # Create a new database session
    db_session = SessionLocal()
    try:
        nearest_warehouse = find_nearest_warehouse(db_session, buyer_location)
        if nearest_warehouse:
            print(f"Nearest warehouse found: {nearest_warehouse.name}")
        else:
            print("No nearby warehouse found")
    except Exception as e:
        print(f"Error processing order created event: {e}")
    finally:
        db_session.close()

# Function to handle 'ProductCreated' event
def on_product_created(ch, method, properties, body):
    print("Received product created event")
    product_data = json.loads(body)
    product_id = product_data.get('product_id')
    product_name = product_data.get('name')
    initial_stock = product_data.get('stock')

    # Create a new database session
    db_session = SessionLocal()
    try:
        add_new_product_to_warehouse(db_session, product_id, product_name, initial_stock)
        print(f"Product {product_name} added to warehouse")
    except Exception as e:
        print(f"Error processing product created event: {e}")
    finally:
        db_session.close()

# Function to handle 'StockUpdated' event
def on_stock_updated(ch, method, properties, body):
    print("Received stock updated event")
    stock_data = json.loads(body)
    product_id = stock_data.get('product_id')
    warehouse_id = stock_data.get('warehouse_id')
    new_quantity = stock_data.get('new_quantity')

    # Create a new database session
    db_session = SessionLocal()
    try:
        update_warehouse_stock(db_session, product_id, warehouse_id, new_quantity)
        print(f"Stock updated for Product ID: {product_id}, Warehouse ID: {warehouse_id}, New Quantity: {new_quantity}")
    except Exception as e:
        print(f"Error processing stock updated event: {e}")
    finally:
        db_session.close()

# Function to handle 'OrderShipped' event
def on_order_shipped(ch, method, properties, body):
    print("Received order shipped event")
    shipment_data = json.loads(body)
    product_id = shipment_data.get('product_id')
    quantity_shipped = shipment_data.get('quantity')
    warehouse_id = shipment_data.get('warehouse_id')

    # Create a new database session
    db_session = SessionLocal()
    try:
        # Adjust inventory after shipment
        update_inventory_after_shipment(db_session, product_id, warehouse_id, quantity_shipped)
        print(f"Order shipped: Product {product_id} - Quantity {quantity_shipped} from Warehouse {warehouse_id}")
    except Exception as e:
        print(f"Error processing order shipped event: {e}")
    finally:
        db_session.close()

# Function to handle 'StockLow' event
def on_stock_low(ch, method, properties, body):
    print("Received stock low event")
    stock_data = json.loads(body)
    product_id = stock_data.get('product_id')
    warehouse_id = stock_data.get('warehouse_id')
    remaining_stock = stock_data.get('remaining_stock')

    # Create a new database session
    db_session = SessionLocal()
    try:
        # Notify the system or perform any actions related to low stock
        notify_stock_low(db_session, product_id, warehouse_id, remaining_stock)
        print(f"Stock low for Product {product_id} in Warehouse {warehouse_id}. Remaining Stock: {remaining_stock}")
    except Exception as e:
        print(f"Error processing stock low event: {e}")
    finally:
        db_session.close()


# Function to start listening to multiple RabbitMQ events
def start_event_listener():
    # Set up the RabbitMQ connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queues (make sure the queues exist)
    channel.queue_declare(queue='order_created')
    channel.queue_declare(queue='product_queue')  # Handles 'product_created' and 'product_updated' events
    channel.queue_declare(queue='stock_queue')    # Handles 'stock_updated' events
    channel.queue_declare(queue='order_shipped')  # Handles 'order_shipped' events
    channel.queue_declare(queue='stock_low')      # Handles 'stock_low' events

    # Start consuming messages for 'OrderCreated' events
    channel.basic_consume(queue='order_created', on_message_callback=on_order_created, auto_ack=True)

    # Start consuming messages for 'ProductCreated' and 'ProductUpdated' events
    channel.basic_consume(queue='product_queue', on_message_callback=on_product_created, auto_ack=True)

    # Start consuming messages for 'StockUpdated' events
    channel.basic_consume(queue='stock_queue', on_message_callback=on_stock_updated, auto_ack=True)

    # Start consuming messages for 'OrderShipped' events
    channel.basic_consume(queue='order_shipped', on_message_callback=on_order_shipped, auto_ack=True)

    # Start consuming messages for 'StockLow' events
    channel.basic_consume(queue='stock_low', on_message_callback=on_stock_low, auto_ack=True)

    print('Waiting for events...')
    channel.start_consuming()
