import httpx
from database.relational_db import get_uow_manually
from database.redis import get_redis, CacheRepo
from service.myfxbook import MyFXService


async def myfx_job():
    async with get_uow_manually() as uow, httpx.AsyncClient(timeout=15) as client:
        cache_repo = CacheRepo(get_redis())
        service = MyFXService(uow, cache_repo, client)
