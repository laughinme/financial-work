from decimal import Decimal
from datetime import datetime, UTC, date as date_
from uuid import UUID
from datetime import timedelta, date
from sqlalchemy import select, update, func, and_
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import array_agg, insert

from domain.payments import TransactionType
from .user_holdings_table import Holding
from .holdings_history import HoldingHistory
from ..portfolios import Portfolio, PortfolioSnapshot
from ...payments import Transaction


class HoldingsInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def insert_snapshot(self, holding: Holding):
        query = (
            insert(HoldingHistory)
            .values(
                user_id=holding.user_id,
                portfolio_id=holding.portfolio_id,
                date=date_.today(),
                units=holding.units,
                total_deposit=holding.total_deposit,
                total_withdraw=holding.total_withdraw,
                current_value=holding.current_value,
                pnl=holding.pnl
            )
            .on_conflict_do_update(
                constraint='uq_holding_history',
                set_={
                    "units": holding.units,
                    "total_deposit": holding.total_deposit,
                    "total_withdraw": holding.total_withdraw,
                    "current_value": holding.current_value,
                    "pnl": holding.pnl
                }
            )
        )
        await self.session.execute(query)
        
    
    async def revalue_holdings(self):
        rows = await self.session.execute(
            select(Holding, Portfolio.nav_price)
            .join(Portfolio, Holding.portfolio_id == Portfolio.id)
            .with_for_update(skip_locked=True)
        )
        
        snap_rows = []
        tx_batch = []
        for holding, nav_price in rows:
            new_val = (holding.units * nav_price).quantize(Decimal("0.00000001"))
            delta = new_val - holding.current_value
            if delta == 0:
                continue

            holding.current_value = new_val
            holding.pnl = new_val - holding.total_deposit + holding.total_withdraw
            
            snap_rows.append(
                dict(
                    user_id = holding.user_id,
                    portfolio_id = holding.portfolio_id,
                    date = date_.today(),
                    units = holding.units,
                    total_deposit = holding.total_deposit,
                    total_withdraw = holding.total_withdraw,
                    current_value = holding.current_value,
                    pnl = holding.pnl,
                )
            )

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
            
        if snap_rows:
            query = insert(HoldingHistory).values(snap_rows)
            query = query.on_conflict_do_update(
                    constraint="uq_holding_history",
                    set_={
                        "units": query.excluded.units,
                        "total_deposit": query.excluded.total_deposit,
                        "total_withdraw": query.excluded.total_withdraw,
                        "current_value": query.excluded.current_value,
                        "pnl": query.excluded.pnl,
                        "updated_at": datetime.now(UTC),
                    }
                )
            await self.session.execute(query)

        if tx_batch:
            self.session.add_all(tx_batch)
        
        
    async def fetch_for_portfolios(
        self, portfolios: list[Portfolio]
    ) -> tuple[dict[int, list[UUID]], dict[int, Decimal]]:
        p_ids = [p.id for p in portfolios]

        query = (
            select(
                Holding.portfolio_id,
                array_agg(func.distinct(Holding.user_id)).label("holders"),
                func.coalesce(func.sum(Holding.total_deposit), 0).label("total_deposit"),
            )
            .where(Holding.portfolio_id.in_(p_ids))
            .group_by(Holding.portfolio_id)
        )
        result = await self.session.execute(query)
        rows = result.all()
        
        holders_map = {pid: user_id for pid, user_id, _ in rows}
        deposit_map = {pid: deposit for pid, _, deposit in rows}

        return holders_map, deposit_map
    
    
    async def holders_and_deposit(self, portfolio_id: int) -> tuple[list[UUID], Decimal]:
        query = (
            select(
                array_agg(func.distinct(Holding.user_id)).label("holders"),
                func.coalesce(func.sum(Holding.total_deposit), 0).label("deposit")
            )
            .where(Holding.portfolio_id == portfolio_id)
        )
        result = await self.session.execute(query)
        row = result.first()
        holders, deposit = row
        
        return holders, deposit
    
    
    async def issue_units(
        self,
        user_id: UUID,
        portfolio_id: int,
        units: Decimal,
        amount: Decimal,
        nav_price: Decimal
    ) -> None:
        new_value = (units * nav_price).quantize(Decimal("0.00000001"))
        
        query = (
            insert(Holding)
            .values(
                user_id=user_id,
                portfolio_id=portfolio_id,
                units=units,
                total_deposit=amount,
                current_value=new_value
            )
            .on_conflict_do_update(
                constraint='pk_portfolio_user',
                set_={
                    "units": Holding.units + units,
                    "total_deposit": Holding.total_deposit + amount,
                    "current_value": Holding.current_value + new_value,
                    "pnl": (
                        Holding.current_value + new_value
                        - (Holding.total_deposit + amount)
                        + Holding.total_withdraw
                    ),
                    "updated_at": datetime.now(UTC)
                }
            )
        )
        await self.session.execute(query)
        
        
    async def burn_units(
        self,
        user_id: UUID,
        portfolio_id: int,
        units: Decimal,
        amount: Decimal
    ) -> bool:
        result = await self.session.execute(
            update(Holding)
            .where(
                Holding.user_id == user_id,
                Holding.portfolio_id == portfolio_id,
                Holding.units >= units
            )
            .values(
                units = Holding.units - units,
                total_withdraw = Holding.total_withdraw + amount,
                current_value = Holding.current_value - amount,
                pnl = (
                    Holding.current_value - amount
                    - Holding.total_deposit
                    + (Holding.total_withdraw + amount)
                ),
            )
            .returning(Holding)
        )
        return result.scalar() is not None

    
    async def user_portfolio_holding(
        self,
        user_id: UUID,
        portfolio_id: int
    ) -> Holding | None:
        query = (
            select(Holding)
            .where(
                Holding.user_id == user_id,
                Holding.portfolio_id == portfolio_id
            )
        )
        holding = await self.session.scalar(query)
        
        return holding

    
    async def user_summary(
        self,
        user_id: UUID
    ) -> dict[str, Decimal | int]:
        Snapshot = aliased(PortfolioSnapshot)
        yesterday = date.today() - timedelta(days=1)

        pnl_subq = (
            select(
                func.coalesce(
                    func.sum(
                        Holding.units * (Portfolio.nav_price - func.coalesce(Snapshot.nav_price, Portfolio.nav_price))), 0,
                )
            )
            .join(Portfolio, Portfolio.id == Holding.portfolio_id)
            .outerjoin(
                Snapshot,
                (Snapshot.portfolio_id == Holding.portfolio_id) & (Snapshot.snapshot_date == yesterday),
            )
            .where(Holding.user_id == user_id)
            .scalar_subquery()
        )

        query = (
            select(
                func.coalesce(func.sum(Holding.current_value), 0).label("total_equity"),
                func.coalesce(func.sum(Holding.pnl), 0).label("total_pnl"),
                func.count().filter(Holding.units > 0).label("portfolios_num"),
                pnl_subq.label("today_pnl"),
            )
            .where(Holding.user_id == user_id)
        )

        result = await self.session.execute(query)
        mapping = result.mappings().first() or {}

        return dict(mapping)


    async def allocation(self, user_id: UUID) -> list:
        total_sub = (
            select(func.coalesce(func.sum(Holding.current_value), 1).label('total'))
            .where(Holding.user_id == user_id)
            .subquery()
        )
        
        query = (
            select(
                Portfolio.id,
                Portfolio.name,
                Holding.current_value,
                (Holding.current_value / total_sub.c.total).label('share'),
                (Holding.current_value / total_sub.c.total * 100).label('percentage')
            )
            .join(Holding, Portfolio.id == Holding.portfolio_id)
            .where(Holding.user_id == user_id)
        )
        result = await self.session.execute(query)
        holdings = result.mappings().all()
        
        return holdings


    async def portfolio_value_series(
        self,
        user_id: UUID,
        days: int
    ) -> list[dict]:
        start = date.today() - timedelta(days=days)

        Snap = aliased(PortfolioSnapshot)
        Units = aliased(HoldingHistory)
        query = (
            select(
                Snap.snapshot_date.label("day"),
                func.sum(Units.units * Snap.nav_price).label("equity")
            )
            .join(Units, and_(
                Units.portfolio_id == Snap.portfolio_id,
                Units.date == Snap.snapshot_date,
                Units.user_id == user_id
            ))
            .where(Snap.snapshot_date >= start)
            .group_by(Snap.snapshot_date)
            .order_by(Snap.snapshot_date)
        )

        rows = (await self.session.execute(query)).all()

        result = []
        prev = None
        for day, eq in rows:
            if prev is None:
                result.append(dict(day=day, equity=eq, daily_pnl=None))
            else:
                result.append(dict(day=day, equity=eq, daily_pnl=eq - prev))
            prev = eq
        return result
