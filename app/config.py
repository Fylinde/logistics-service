import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Settings:
    
    RABBITMQ_HOST: str = "rabbitmq"  # Default to the RabbitMQ service name in Docker Compose
    RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
    
    SECURITY_PASSWORD_SALT: str = os.getenv("SECURITY_PASSWORD_SALT", "mX-rk2vC6fyBmWPncH54sbHVLv4dT0FqQE2mysbkeKM")

    # Email configurations for sending notifications
    GMAIL_USER: str = os.getenv("GMAIL_USER", "fylinde.marketplace@gmail.com")
    GMAIL_PASSWORD: str = os.getenv("GMAIL_PASSWORD", "mmzm fpjh opgh aozk")
    
    # Logistics team email
    LOGISTICS_TEAM_EMAIL = os.getenv("LOGISTICS_TEAM_EMAIL", "logistics-team@yourdomain.com")

    SECRET_KEY = os.getenv("SECRET_KEY", "DbSLoIREJtu6z3CVnpTd_DdFeMMRoteCU0UjJcNreZI")
    PROJECT_NAME: str = "Logistics Service"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Sylvian@db:5433/logistics_service_db")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "Sylvian")
    DATABASE_DB: str = os.getenv("DATABASE_DB", "logistics_service_db")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5433"))

settings = Settings()
