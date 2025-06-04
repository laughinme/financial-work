import logging

from decimal import Decimal
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from datetime import date

from database.relational_db import (
    UoW,
    Portfolio,
    PortfolioInterface,
    GainsInterface,
    HoldingsInterface
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
        portfolio_repo: PortfolioInterface,
        gains_repo: GainsInterface,
        holdings_repo: HoldingsInterface
    ):
        self.uow, self.portfolio_repo, self.gains_repo = uow, portfolio_repo, gains_repo
        self.holdings_repo = holdings_repo
        
    
    async def list_all(self, size: int, page: int, with_charts: bool = False) -> list:
        portfolios = await self.portfolio_repo.list_all(size, page)
        holders, deposits = await self.holdings_repo.fetch_for_portfolios(portfolios)
        if with_charts:
            sparklines = await self.gains_repo.fetch_sparklines(portfolios)
            
            for p in portfolios:
                p.sparkline_gain = sparklines.get(p.id, [])
            
        for p in portfolios:
            p.holders = holders.get(p.id, 0)
            p.deposit = deposits.get(p.id, Decimal('0'))
            p.duration = (date.today() - p.first_trade_at.date()).days
            
        return portfolios
    
    
    async def get_specific(self, portfolio_id: int):
        p = await self.portfolio_repo.get_by_id(portfolio_id)
        holders, deposits = await self.holdings_repo.holders_and_deposit(portfolio_id)
        
        p.holders = holders
        p.deposit = deposits
        p.duration = (date.today() - p.first_trade_at.date()).days
        
        return p
        
    
    async def get_history(self, portfolio_id: int, days: int):
        balance_equity, drawdown = await self.portfolio_repo.get_snapshot_history(portfolio_id, days)
        gains = await self.gains_repo.gain_history(portfolio_id, days)
        
        return {
            'sparkline': gains,
            'balance_equity': balance_equity,
            'drawdown': drawdown
        }
