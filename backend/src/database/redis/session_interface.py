import json
from redis.asyncio import Redis

class SessionRepo():
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def set(self, session_id: str, payload: dict, ttl: int) -> None:
        data = json.dumps(payload)
        await self.redis.set(session_id, data, ex=ttl)
        
    async def get(self, session_id: str) -> dict | None:
        data = await self.redis.get(session_id)
        return json.loads(data) if data else None
    
    async def delete(self, session_id: str) -> None:
        await self.redis.delete(session_id)
        
    async def update(self, session_id: str, ttl: int) -> None:
        await self.redis.expire(session_id, ttl)
