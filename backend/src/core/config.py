from pathlib import Path
from pydantic import model_validator

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR  = Path(__file__).resolve().parent.parent.parent

class Config(BaseSettings):
    """
    Project dependencies config
    """
    # API settings
    API_PORT: int = 8000
    API_HOST: str = '0.0.0.0'
    
    # Auth Settings
    SESSION_TTL: int = 60 * 60 * 24 * 14 # Session will expire in 14 days
    SESSION_SECRET_KEY: str
    
    JWT_PRIVATE_KEY: str = ''
    JWT_PUBLIC_KEY: str = ''
    JWT_ALGO: str = 'RS256'
    ACCESS_TTL: int = 60 * 15
    REFRESH_TTL: int = 60 * 60 * 24 * 7
    
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
    
    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/.env')

    @model_validator(mode='before')
    @classmethod
    def load_jwt_keys(cls, raw):
        data = dict(raw)
        
        priv_file = Path("/run/secrets/jwt_private_key.pem")
        if priv_file.is_file() and not data.get("JWT_PRIVATE_KEY"):
            data["JWT_PRIVATE_KEY"] = priv_file.read_text()
            
        pub_file = Path("/run/secrets/jwt_public_key.pem")
        if pub_file.is_file() and not data.get("JWT_PUBLIC_KEY"):
            data["JWT_PUBLIC_KEY"] = pub_file.read_text()
            
        return data
