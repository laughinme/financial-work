import logging

from uuid import UUID
from decimal import Decimal
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from datetime import date

from database.relational_db import (
    UoW,
    PortfolioInterface,
    GainsInterface,
    HoldingsInterface,
    InvestOrderInterface
)
from database.redis import CacheRepo
from domain.investments import InvestOrderStatus
from core.config import Config

config = Config()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PortfolioService:
    def __init__(
        self,
        uow: UoW,
        p_repo: PortfolioInterface,
        g_repo: GainsInterface,
        h_repo: HoldingsInterface,
        io_repo: InvestOrderInterface
    ):
        self.uow, self.p_repo, self.g_repo = uow, p_repo, g_repo
        self.h_repo, self.io_repo = h_repo, io_repo
        
    
    async def list_all(self, user_id: UUID, size: int, page: int, with_charts: bool = False) -> list:
        portfolios = await self.p_repo.list_all(size, page)
        holders, deposits = await self.h_repo.fetch_for_portfolios(portfolios)
        user_holdings = await self.h_repo.user_holdings_map(
            user_id, [p.id for p in portfolios]
        )
        if with_charts:
            sparklines = await self.g_repo.fetch_sparklines(portfolios)
            
            for p in portfolios:
                p.sparkline_gain = sparklines.get(p.id, [])
            
        for p in portfolios:
            holder_ids = holders.get(p.id, [])
            p.holders = len(holder_ids)
            p.deposit = deposits.get(p.id, Decimal('0'))
            p.duration = (date.today() - p.first_trade_at.date()).days
            p.invested_by_user = user_id in holder_ids

            holding = user_holdings.get(p.id)
            if holding:
                p.user_units = holding.units
                p.user_value = holding.current_value
                p.user_share = (
                    (holding.units / p.units_total * Decimal('100'))
                    if p.units_total
                    else None
                )
            else:
                p.user_units = None
                p.user_value = None
                p.user_share = None
            
        return portfolios
    
    
    async def get_specific(self, user_id: UUID, portfolio_id: int):
        p = await self.p_repo.get_by_id(portfolio_id)
        holder_ids, deposits = await self.h_repo.holders_and_deposit(portfolio_id)
        holding = await self.h_repo.user_portfolio_holding(user_id, portfolio_id)

        p.holders = len(holder_ids)
        p.deposit = deposits
        p.duration = (date.today() - p.first_trade_at.date()).days
        p.invested_by_user = user_id in holder_ids

        if holding:
            p.user_units = holding.units
            p.user_value = holding.current_value
            p.user_share = (
                (holding.units / p.units_total * Decimal('100'))
                if p.units_total
                else None
            )
        else:
            p.user_units = None
            p.user_value = None
            p.user_share = None

        return p
        
    
    async def get_history(self, portfolio_id: int, days: int):
        balance_equity, drawdown = await self.p_repo.get_snapshot_history(portfolio_id, days)
        gains = await self.g_repo.gain_history(portfolio_id, days)
        
        return {
            'sparkline': gains,
            'balance_equity': balance_equity,
            'drawdown': drawdown
        }
