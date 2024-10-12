from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
import pika
#from app.database import engine, SessionLocal
#from app.models import WarehouseModel, StockModel
from app.routes import logistics

# Create tables (only needed in development, you can use Alembic for production migrations)
#from app.models.warehouse import WarehouseModel
from app.models.stock import StockModel
from app.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with Swagger UI metadata
app = FastAPI(
    title="Logistics Service API",
    description="API for managing warehouses, inventory, and logistics operations",
    version="1.0.0",
    docs_url="/docs",  # Default URL for Swagger UI
    redoc_url="/redoc",  # Optional: ReDoc UI for alternative documentation interface
)

# Set up CORS (you can update this list with the allowed origins)
origins = [
    "http://localhost",
    "http://localhost:3000",  # Example for frontend running locally
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables (you can also manage migrations using Alembic)
#WarehouseModel.metadata.create_all(bind=engine)
#StockModel.metadata.create_all(bind=engine)


# Include logistics-related routes from the routes/logistics.py module
app.include_router(logistics.router, prefix="/logistics", tags=["Logistics"])

# Root path to check the health of the service
@app.get("/")
def read_root():
    return {"message": "Logistics Service is running"}


# Startup event to check RabbitMQ connection
@app.on_event("startup")
async def startup_event():
    try:
        # Attempt to connect to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)  # Use RabbitMQ host from settings
        )
        connection.close()
        logger.info("Successfully connected to RabbitMQ")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")

    # Print all routes in the application (for debugging purposes)
    for route in app.router.routes:
        print(route.path, route.name)


# Optional shutdown event if you want to cleanly close resources
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Logistics Service is shutting down.")