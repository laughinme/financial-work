import json
import asyncio
import logging
import httpx

from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from datetime import date

from database.relational_db import (
    UoW
)
from database.redis import CacheRepo
from domain.myfxbook import DataDailySchema, AccountsSchema, DailyGainSchema
from core.config import Config
from .exceptions import MyFXError


config = Config()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyFXService:
    BASE_URL = 'https://www.myfxbook.com/api'
    
    def __init__(
        self,
        uow: UoW,
        cache_repo: CacheRepo,
        client: httpx.AsyncClient
    ):
        self.uow, self.cache_repo, self.client = uow, cache_repo, client


    async def _get_session(self) -> str:
        if session := await self.cache_repo.get('myfx:session'):
            return session
        
        response = await self._call('/login.json', params={
            'email': config.MYFXBOOK_LOGIN,
            'password': config.MYFXBOOK_PASSWORD
        }, with_retry=False)
        session = response['session']
        
        await self.cache_repo.set('myfx:session', session, ttl=3600*24)
        
        return session


    async def _call(
        self,
        path: str,
        params: dict[str, str],
        with_retry: bool = True
    ):
        url = f"{self.BASE_URL}{path}"
        for attempt in range(3):
            try:
                response = await self.client.get(url, params=params, timeout=15)
                response.raise_for_status()
                data: dict = response.json()
                if data.get('error'):
                    raise MyFXError(data['message'])
                
                return data
            except MyFXError:
                if not with_retry or attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)


    async def logout(self) -> None:
        session = await self._get_session()
        await self._call('/logout.json', params={'session': session})        
        
        await self.cache_repo.delete('myfx:session')


    async def get_accounts(self) -> AccountsSchema:
        cache_key = "myfx:accounts"
        if raw := await self.cache_repo.get(cache_key):
            return AccountsSchema.model_validate(raw)
        
        session = await self._get_session()
        response = await self._call('/get-my-accounts.json', params={'session': session})
        await self.cache_repo.set(cache_key, response, ttl=15*60)
        
        return AccountsSchema.model_validate(response)


    async def get_data_daily(
        self, account_id: str, start: date, end: date,
    ) -> DataDailySchema:
        cache_key = f"myfx:data_daily:{account_id}:{start}:{end}"
        if (raw := await self.cache_repo.get(cache_key)):
            return DataDailySchema.model_validate(raw)
        
        session = await self._get_session()
        data = await self._call(
            '/get-data-daily.json',
            params={'session': session, 'id': account_id, 'start': start, 'end': end}
        )
        
        await self.cache_repo.set(cache_key, json.dumps(data), ttl=60*60)
        return DataDailySchema.model_validate(data)
    
    
    async def bulk_data_daily(
        self, *account_ids: str, start: date, end: date
    ) -> list[DataDailySchema]:
        tasks = [self.get_data_daily(account_id, start, end) for account_id in account_ids]
        return await asyncio.gather(*tasks)


    async def get_daily_gain(
        self, account_id: str, start: date, end: date,
    ) -> DailyGainSchema:
        cache_key = f'myfx:daily_gain:{account_id}:{start}:{end}'
        if raw := await self.cache_repo.get(cache_key):
            return DailyGainSchema.model_validate(raw)
            
        session = await self._get_session()
        data = await self._call(
            '/get-daily-gain.json',
            params={'session': session, 'id': account_id, 'start': start, 'end': end}
        )
        
        await self.cache_repo.set(cache_key, json.dumps(data), ttl=15*60)
        return DailyGainSchema.model_validate(data)
    

    async def bulk_daily_gain(
        self, *account_ids: str, start: date, end: date
    ) -> list[DataDailySchema]:
        tasks = [self.get_daily_gain(account_id, start, end) for account_id in account_ids]
        return await asyncio.gather(*tasks)
