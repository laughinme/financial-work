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

    # Site data (url, paths)
    SITE_URL: str
    
    # External services data
    MYFXBOOK_LOGIN: str
    MYFXBOOK_PASSWORD: str
    
    class Config:
        env_file = f'{BASE_DIR}/.env'
