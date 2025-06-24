from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR  = Path(__file__).resolve().parent.parent.parent

class Config(BaseSettings):
    """
    Project dependencies config
    """
    # API settings
    API_PORT: int = 8000
    API_HOST: str = '0.0.0.0'
    SESSION_LIFETIME: int = 60*60*24*14 # Session will expire in 14 days
    SESSION_SECRET_KEY: str
    
    # Database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    
    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int
    
    # Telegram bot settings
    BOT_TOKEN: str

    # Payment system settings
    YOOKASSA_ACCOUNT_ID: str
    YOOKASSA_SECRET: str
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    # Site data (url, paths)
    SITE_URL: str
    
    # External services data
    MOCK_URL: str = 'http://localhost:8001/api/v1'
    MYFXBOOK_URL: str = 'https://www.myfxbook.com/api'
    MYFXBOOK_LOGIN: str
    MYFXBOOK_PASSWORD: str
    
    class Config:
        env_file = f'{BASE_DIR}/.env'
