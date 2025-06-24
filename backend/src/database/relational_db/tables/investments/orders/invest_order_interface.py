from decimal import Decimal
from collections import defaultdict
from sqlalchemy import select, update, func, case
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from domain.investments import InvestOrderStatus, OrderDirection
from .invest_order_table import InvestOrder
from ..portfolios import Portfolio


class InvestOrderInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def add(self, order: InvestOrder) -> None:
        self.session.add(order)
    
    
    async def get_by_pids(
        self, p_ids: set[int], status: InvestOrderStatus = InvestOrderStatus.ACCEPTED
    ) -> list[InvestOrder]:
        orders = await self.session.scalars(
            select(InvestOrder)
            .where(
                InvestOrder.portfolio_id.in_(p_ids),
                InvestOrder.status == status
            )
            .order_by(InvestOrder.created_at)
            .with_for_update(skip_locked=True)
        )
        
        return orders.all()
    
    
    async def get_by_pid(
        self, p_id: int, status: InvestOrderStatus = InvestOrderStatus.PENDING
    ) -> list[InvestOrder]:
        orders = await self.session.scalars(
            select(InvestOrder)
            .where(
                InvestOrder.portfolio_id == p_id,
                InvestOrder.status == status
            )
            .order_by(InvestOrder.created_at)
            .with_for_update(skip_locked=True)
        )
        
        return orders.all()


    async def list_orders(self, status: InvestOrderStatus) -> list[InvestOrder]:
        orders = await self.session.scalars(
            select(InvestOrder)
            .where(InvestOrder.status == status)
            .order_by(InvestOrder.created_at)
            .group_by(InvestOrder.portfolio_id, InvestOrder.id)
            # .with_for_update(skip_locked=True)
        )
        
        # grouped = defaultdict(list)
        # for order in orders.all():
        #     grouped[order.portfolio_id].append(order)
            
        # return dict(grouped)
        
        return orders.all()
    
    
    async def portfolio_deposit_withdrawal(self, p_id: int) -> dict[str, Decimal]:
        """Pending deposits are stored in dollars whereas withdrawals are stored
        as portfolio units. This helper returns both values in dollars."""

        query = (
            select(
                func.sum(
                    case((InvestOrder.direction == OrderDirection.INVEST, InvestOrder.amount), else_=0)
                ).label('deposits'),
                func.sum(
                    case((InvestOrder.direction == OrderDirection.PAYBACK, InvestOrder.units), else_=0)
                ).label('withdraw_units')
            )
            .where(
                InvestOrder.status == InvestOrderStatus.PENDING,
                InvestOrder.portfolio_id == p_id
            )
        )

        result = await self.session.execute(query)
        amounts = result.mappings().first()
        deposits = amounts['deposits'] or Decimal('0')
        withdraw_units = amounts['withdraw_units'] or Decimal('0')

        nav_price = await self.session.scalar(
            select(Portfolio.nav_price).where(Portfolio.id == p_id)
        )
        withdrawals = (withdraw_units * nav_price).quantize(Decimal('0.00000001'))

        return {
            'deposits': deposits,
            'withdrawals': withdrawals,
            'delta': deposits - withdrawals,
        }
    
    
    async def aggregated_orders(
        self,
        portfolio_ids: list[int],
        quantity: int,
    ) -> dict[int, list[InvestOrder]]:
        if not portfolio_ids:
            return {}

        sub = (
            select(
                InvestOrder,
                func.row_number()
                .over(
                    partition_by=InvestOrder.portfolio_id,
                    order_by=InvestOrder.created_at.desc()
                ).label("rk")
            )
            .where(
                InvestOrder.portfolio_id.in_(portfolio_ids),
                InvestOrder.status == InvestOrderStatus.PENDING
            )
            .subquery()
        )

        Inv = aliased(InvestOrder, sub)

        query = (
            select(Inv)
            .where(sub.c.rk <= quantity)
            .order_by(Inv.portfolio_id, Inv.created_at.desc())
        )

        grouped: dict[int, list[InvestOrder]] = defaultdict(list)
        for order in (await self.session.scalars(query)).all():
            grouped[order.portfolio_id].append(order)

        return grouped
    
    
    async def settlements_brief(self) -> list[dict]:
        """Return a short summary of pending settlement orders.

        The ``withdraw`` and ``delta`` values represent dollar amounts. PAYBACK
        orders are converted from units using the portfolio NAV price.
        """
        invest_case = case(
            (InvestOrder.direction == OrderDirection.INVEST, InvestOrder.amount),
            else_=0,
        )
        withdraw_case = case(
            (InvestOrder.direction == OrderDirection.PAYBACK, InvestOrder.units * Portfolio.nav_price),
            else_=0,
        )
        
        query = (
            select(
                Portfolio.id.label('portfolio_id'),
                Portfolio.name,
                func.sum(invest_case).label("invest"),
                func.sum(withdraw_case).label("withdraw"),
                (func.sum(invest_case) - func.sum(withdraw_case)).label("delta"),
            )
            .join(InvestOrder, InvestOrder.portfolio_id == Portfolio.id)
            .where(InvestOrder.status == InvestOrderStatus.PENDING)
            .group_by(Portfolio.id, Portfolio.name)
            .order_by(Portfolio.name)
        )
        
        rows = (await self.session.execute(query)).mappings().all()
        return [dict(r) for r in rows]
