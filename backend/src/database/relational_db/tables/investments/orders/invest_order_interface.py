from decimal import Decimal
from datetime import  datetime, UTC, date
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from domain.investments import InvestOrderStatus
from .invest_order_table import InvestOrder
from ..portfolios import Portfolio
from ...payments import Transaction


class InvestOrderInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def add(self, order: InvestOrder) -> None:
        self.session.add(order)
    
    
    async def get_by_pids(self, p_ids: set[int]) -> list[InvestOrder]:
        orders = await self.session.scalars(
            select(InvestOrder)
            .where(
                InvestOrder.portfolio_id.in_(p_ids),
                InvestOrder.status == InvestOrderStatus.PENDING
            )
            .order_by(InvestOrder.created_at)
            .with_for_update(skip_locked=True)
        )
        
        return orders.all()


    async def list(self, status: InvestOrderStatus) -> list[InvestOrder]:
        orders = await self.session.scalars(
            select(InvestOrder)
            .where(InvestOrder.status == status)
            # .order_by(InvestOrder.created_at)
            .with_for_update(skip_locked=True)
        )
        
        return orders.all()
