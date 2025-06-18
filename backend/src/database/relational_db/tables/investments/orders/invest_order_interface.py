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
        query = (
            select(
                func.sum(
                    case((InvestOrder.direction == OrderDirection.INVEST, InvestOrder.amount), else_=0)
                ).label('deposits'),
                func.sum(
                    case((InvestOrder.direction == OrderDirection.PAYBACK, InvestOrder.amount), else_=0)
                ).label('withdrawals'),
                (
                    func.sum(
                        case((InvestOrder.direction == OrderDirection.INVEST, InvestOrder.amount), else_=0)
                    )
                    -
                    func.sum(
                        case((InvestOrder.direction == OrderDirection.PAYBACK, InvestOrder.amount), else_=0)
                    )
                ).label('delta')
            )
            .where(
                InvestOrder.status == InvestOrderStatus.PENDING,
                InvestOrder.portfolio_id == p_id
            )
        )
        result = await self.session.execute(query)
        return dict(result.mappings().first())
    
    
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
        query = (
            select(
                Portfolio.id.label('portfolio_id'),
                Portfolio.name,
                func.sum(
                    case(
                        (InvestOrder.direction == OrderDirection.INVEST, InvestOrder.amount),
                        else_=0,
                    )
                ).label("invest"),
                func.sum(
                    case(
                        (InvestOrder.direction == OrderDirection.PAYBACK, InvestOrder.amount),
                        else_=0,
                    )
                ).label("withdraw"),
                (
                    func.sum(
                        case((InvestOrder.direction == OrderDirection.INVEST, InvestOrder.amount), else_=0)
                    )
                    -
                    func.sum(
                        case((InvestOrder.direction == OrderDirection.PAYBACK, InvestOrder.amount), else_=0)
                    )
                ).label("delta"),
            )
            .join(InvestOrder, InvestOrder.portfolio_id == Portfolio.id)
            .where(InvestOrder.status == InvestOrderStatus.PENDING)
            .group_by(Portfolio.id, Portfolio.name)
            .order_by(Portfolio.name)
        )
        
        rows = (await self.session.execute(query)).mappings().all()
        return [dict(r) for r in rows]
