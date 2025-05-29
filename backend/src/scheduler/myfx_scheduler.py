from database.relational_db import get_uow_manually
from database.redis import get_redis, CacheRepo
from service.myfxbook import MyFXService


async def myfx_job():
    async with get_uow_manually() as uow:
        cache_repo = CacheRepo(get_redis())
        service = MyFXService(uow, cache_repo)
        
        
        
