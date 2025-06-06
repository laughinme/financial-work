from decimal import Decimal
from uuid import UUID
from datetime import  datetime, UTC, date
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from domain.payments import TransactionType
from .user_holdings_table import Holding
from ..portfolios import Portfolio
from ...payments import Transaction


class HoldingsInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def revalue_holdings(self):
        rows = await self.session.execute(
            select(Holding, Portfolio.nav_price)
            .join(Portfolio, Holding.portfolio_id == Portfolio.id)
            .with_for_update(skip_locked=True)
        )
        
        tx_batch = []
        for holding, nav_price in rows:
            new_val = (holding.units * nav_price).quantize(Decimal("0.00000001"))
            delta = new_val - holding.current_value
            if delta == 0:
                continue

            holding.current_value = new_val
            holding.pnl = new_val - holding.total_deposit + holding.total_withdraw

            tx_batch.append(
                Transaction(
                    user_id = holding.user_id,
                    portfolio_id = holding.portfolio_id,
                    amount = delta,
                    currency = holding.portfolio.currency,
                    type = TransactionType.PNL,
                    comment = "Mark to Market revaluation"
                )
            )

        if tx_batch:
            self.session.add_all(tx_batch)
        
        
    async def fetch_for_portfolios(self, portfolios: list[Portfolio]):
        p_ids = [p.id for p in portfolios]

        query = (
            select(Holding.portfolio_id, func.count().label("_count"),
                func.coalesce(func.sum(Holding.total_deposit), 0).label("deposit"))
            .where(Holding.portfolio_id.in_(p_ids))
            .group_by(Holding.portfolio_id)
        )
        rows = await self.session.execute(query)
        holders_map = {pid: row._count for pid, row, _ in rows}
        deposit_map = {pid: row.deposit for pid, _, row in rows}

        return holders_map, deposit_map
    
    
    async def holders_and_deposit(self, portfolio_id: int) -> tuple[int, Decimal]:
        query = (
            select(
                func.count().label("_count"),
                func.coalesce(func.sum(Holding.total_deposit), 0).label("deposit")
            )
            .where(Holding.portfolio_id == portfolio_id)
        )
        result = await self.session.execute(query)
        row = result.first()
        holders, deposit = row
        
        return holders, deposit
    
    
    async def issue_units(self, user_id: UUID, units: Decimal, deposit: Decimal):
        await self.session.execute(
            update(Holding)
            .where(Holding.user_id == user_id)
            .values(
                units = Holding.units + units,
                total_deposit = Holding.total_deposit + deposit,
            )
        )
