from fastapi import Depends
from redis.asyncio import Redis

from database.redis import SessionRepo, get_redis
from .session_service import SessionService


async def get_session_service(
    redis: Redis = Depends(get_redis)
) -> SessionService:
    session_repo = SessionRepo(redis)
    return SessionService(session_repo)
