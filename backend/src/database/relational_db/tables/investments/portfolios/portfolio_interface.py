from contextlib import asynccontextmanager
from decimal import Decimal
from datetime import datetime, UTC, date, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from .portfolios_table import Portfolio
from .portfolio_snapshots_table import PortfolioSnapshot
from domain.myfxbook import AccountSchema


class PortfolioInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    # helpers
    @staticmethod
    def _portfolio_row(
        portfolio_id: int,
        acc: AccountSchema,
        nav_price: Decimal,
        units_total: Decimal | None = None,
    ) -> dict:
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
            deposits = acc.deposits,
            withdrawals = acc.withdrawals,
            invitation_url = acc.invitation_url,
            gain_percent = acc.gain,
            net_profit = acc.profit,
            first_trade_at = acc.first_trade_date,
            last_sync = datetime.now(UTC),
            last_update_myfx = acc.last_update_date
        )
        if portfolio_id:
            p_dict['id'] = portfolio_id
        
        if units_total is not None:
            p_dict['units_total'] = units_total
            
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
    
    
    @asynccontextmanager
    async def get_isolated(self, portfolio_id: int):
        p = await self.session.get(Portfolio, portfolio_id, with_for_update=True)
        yield p
    
    
    async def list_all(self, size: int = 0, page: int = 0) -> list[Portfolio]:
        portfolios = await self.session.scalars(
            select(Portfolio)
            # .where(Portfolio.active == True)
            .offset((page - 1) * size)
            .limit(size or None)
        )
        return portfolios.all()
        
        
    async def get_snapshot_history(
        self, portfolio_id: int, days: int
    ) -> tuple[list[dict], list[dict]]:
        query = (
            select(
                PortfolioSnapshot.snapshot_date,
                PortfolioSnapshot.balance,
                PortfolioSnapshot.equity,
                PortfolioSnapshot.drawdown
            )
            .where(
                PortfolioSnapshot.portfolio_id == portfolio_id,
                PortfolioSnapshot.snapshot_date >= date.today() - timedelta(days=days)
            )
            .order_by(PortfolioSnapshot.snapshot_date)
        )
        result = await self.session.execute(query)
        rows = result.all()
        
        balance_equity = []
        drawdown_hist = []
        for _date, balance, equity, drawdown in rows:
            balance_equity.append({'date': _date, 'balance': balance, 'equity': equity})
            drawdown_hist.append({'date': _date, 'drawdown': drawdown})
        
        return balance_equity, drawdown_hist
    

    async def bulk_insert_from_accounts(self, accounts: list[AccountSchema]) -> list[Portfolio]:
        rows = [self._portfolio_row(None, a, Decimal('1'), Decimal('0')) for a in accounts]
        result = await self.session.execute(
            insert(Portfolio).values(rows).returning(Portfolio)
        )
        return list(result.scalars().all())


    async def bulk_upsert(self, rows: list[dict], chunk_size: int = 1000):
        if not rows:
            return
        for i in range(0, len(rows), chunk_size):
            batch = rows[i:i + chunk_size]
            query = insert(Portfolio).values(batch)
            query = query.on_conflict_do_update(
                index_elements=["oid_myfx"],
                set_={c: getattr(query.excluded, c) for c in batch[0] if c != "id"}
            )
            await self.session.execute(query)

    
    async def bulk_upsert_snapshots(self, rows: list[dict], chunk_size: int = 1000):
        if not rows:
            return
        for i in range(0, len(rows), chunk_size):
            batch = rows[i:i + chunk_size]
            query = insert(PortfolioSnapshot).values(batch)
            query = query.on_conflict_do_update(
                index_elements=["portfolio_id", "snapshot_date"],
                set_={
                    "nav_price": query.excluded.nav_price,
                    "balance": query.excluded.balance,
                    "equity": query.excluded.equity,
                    "drawdown": query.excluded.drawdown,
                    "updated_at": datetime.now(UTC),
                },
            )
            await self.session.execute(query)
