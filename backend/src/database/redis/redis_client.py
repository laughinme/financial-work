from contextlib import asynccontextmanager
from typing import AsyncGenerator
from redis.asyncio import Redis
from core.config import Config

config = Config()

redis_client = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT
)

async def get_redis() -> AsyncGenerator[Redis, None]:
    "Returns prepared Redis session"
    yield redis_client
    

async def get_redis_manually() -> Redis:
    return redis_client
