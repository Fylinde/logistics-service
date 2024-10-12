# app/services/product_service_client.py

import requests
from app.config import settings

PRODUCT_SERVICE_BASE_URL = settings.PRODUCT_SERVICE_URL  # Set in settings as the Product-Service base URL

def get_product_stock(product_id, warehouse_id):
    """
    Fetch product stock from the Product-Service via HTTP API.
    """
    url = f"{PRODUCT_SERVICE_BASE_URL}/products/{product_id}/stock?warehouse_id={warehouse_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Return stock data
        else:
            print(f"Failed to fetch stock data from Product-Service. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching product stock: {e}")
        return None
def update_product_stock_in_product_service(product_id, warehouse_id, new_quantity):
    """
    Update product stock in the Product-Service via HTTP API.
    """
    url = f"{PRODUCT_SERVICE_BASE_URL}/products/{product_id}/stock/{warehouse_id}"
    data = {"new_quantity": new_quantity}
    try:
        response = requests.put(url, json=data)
        return response.status_code == 200  # Return True if the update was successful
    except Exception as e:
        print(f"Error updating product stock in Product-Service: {e}")
        return False