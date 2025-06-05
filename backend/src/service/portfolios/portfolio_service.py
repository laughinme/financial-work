import json
import asyncio
import logging
import httpx

from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from datetime import date

from domain.myfxbook import AccountsSchema
from database.relational_db import (
    UoW,
    Portfolio,
    PortfolioInterface
)
from database.redis import CacheRepo
from core.config import Config


config = Config()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PortfolioService:
    BASE_URL = 'https://www.myfxbook.com/api'
    
    def __init__(
        self,
        uow: UoW,
        portfolio_repo: PortfolioInterface
    ):
        self.uow, self.portfolio_repo = uow, portfolio_repo
        
    
    async def get_all(self, size: int, page: int) -> list[Portfolio]:
        portfolios = await self.portfolio_repo.list_all(size, page)
        return portfolios
