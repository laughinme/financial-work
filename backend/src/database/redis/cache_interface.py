from redis.asyncio import Redis


class CacheRepo():
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def set(self, name: str, value: str, ttl: int | None = None) -> None:
        await self.redis.set(name, value, ex=ttl)
        
    async def get(self, name: str) -> str | None:
        data = await self.redis.get(name)
        return data
    
    async def delete(self, *names: str) -> None:
        await self.redis.delete(*names)
        
    async def update(self, name: str, ttl: int) -> None:
        await self.redis.expire(name, ttl)
