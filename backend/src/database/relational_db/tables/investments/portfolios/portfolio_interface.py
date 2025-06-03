from decimal import Decimal
from datetime import  datetime, UTC, date
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from .portfolios_table import Portfolio
from .portfolio_snapshots_table import PortfolioSnapshot
from ..holdings import Holding
from .daily_gains_table import DailyGain
from domain.myfxbook import AccountSchema, DayGain


class PortfolioInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    # helpers
    @staticmethod
    def _portfolio_row(p_id: int, acc: AccountSchema, nav_price: Decimal) -> dict:
        p_dict = dict(
            oid_myfx = acc.id,
            account_number = acc.account_id,
            name = acc.name,
            description = acc.description,
            broker = acc.server.name,
            currency = acc.currency,
            nav_price = nav_price,
            balance = acc.balance,
            equity = acc.equity,
            drawdown = acc.drawdown,
            gain_percent = acc.gain,
            net_profit = acc.profit,
            first_trade_at = acc.first_trade_date,
            last_sync = datetime.now(UTC)
        )
        if p_id:
            p_dict['id'] = p_id
            
        return p_dict
    
    @staticmethod
    def _snapshot_row(
        portfolio_id: int,
        sh_date: date,
        nav: Decimal,
        balance: Decimal, 
        equity: Decimal,
        drawdown: Decimal
    ) -> dict:
        return dict(
            portfolio_id = portfolio_id,
            snapshot_date = sh_date,
            nav_price = nav,
            balance = balance,
            equity = equity,
            drawdown = drawdown
        )

    @staticmethod
    def _gain_row(portfolio_id: int, gain: DayGain) -> dict:
        return dict(
            portfolio_id = portfolio_id,
            date = gain.date,
            gain_pct = gain.value,
            profit = gain.profit,
        )


    async def add(
        self, 
        portfolio: Portfolio
    ) -> None:
        self.session.add(portfolio)

    
    async def insert(
        self,
        data: list[Portfolio]
    ) -> list[Portfolio]:
        query = insert(Portfolio).values([portfolio.__dict__ for portfolio in data])
        query.on_conflict_do_update(
            index_elements=['oid_myfx'],
            set_={c: query.excluded[c] for c in data[0].__dict__.keys() if c != "id"}
        ).returning(Portfolio)
        result = await self.session.execute(query)
        
        return await result.scalars().all()
    

    async def get_by_id(
        self,
        portfolio_id: int
    ) -> Portfolio | None:
        portfolio = await self.session.get(Portfolio, portfolio_id)
        return portfolio
    
    
    async def list_all(self, size: int = 0, page: int = 0) -> list[Portfolio]:
        portfolios = await self.session.scalars(
            select(Portfolio)
            # .where(Portfolio.active == True)
            .offset((page - 1) * size)
            .limit(size or None)
        )
        return portfolios.all()


    async def bulk_insert_from_accounts(self, accounts: list[AccountSchema]) -> list[Portfolio]:
        rows = [self._portfolio_row(None, a, Decimal('1')) for a in accounts]
        result = await self.session.execute(
            insert(Portfolio).values(rows).returning(Portfolio)
        )
        return list(result.scalars().all())


    async def bulk_upsert(self, rows: list[dict]):
        if not rows:
            return
        query = insert(Portfolio).values(rows)
        query = query.on_conflict_do_update(
            index_elements=["oid_myfx"],
            set_={c: getattr(query.excluded, c) for c in rows[0] if c != "id"}
        )
        await self.session.execute(query)

    
    async def bulk_upsert_snapshots(self, rows: list[dict]):
        if not rows:
            return
        query = insert(PortfolioSnapshot).values(rows)
        query = query.on_conflict_do_update(
            index_elements=["portfolio_id", "snapshot_date"],
            set_= {
                "nav_price": query.excluded.nav_price,
                "balance": query.excluded.balance,
                "equity": query.excluded.equity,
                "drawdown": query.excluded.drawdown,
                "updated_at": datetime.now(UTC)
            }
        )
        await self.session.execute(query)

    
    async def bulk_upsert_gains(self, rows: list[dict]):
        if not rows:
            return
        query = insert(DailyGain).values(rows)
        query = query.on_conflict_do_update(
            index_elements=["portfolio_id", "date"],
            set_= {
                "gain_pct": query.excluded.gain_pct,
                "profit":   query.excluded.profit,
            }
        )
        await self.session.execute(query)
        
    
    async def revalue_holdings(self):
        query = (
            update(Holding)
            .values(
                current_value = Holding.units * Portfolio.nav_price,
                pnl = (Holding.units * Portfolio.nav_price)
                - Holding.total_deposit
                + Holding.total_withdraw,
            )
            .where(Holding.portfolio_id == Portfolio.id)
        )

        await self.session.execute(query)
