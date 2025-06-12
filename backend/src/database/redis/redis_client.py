from redis.asyncio import Redis
from core.config import Config

config = Config()

redis_client = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    decode_responses=True
)

def get_redis() -> Redis:
    """Returns prepared Redis session"""
    return redis_client
    
