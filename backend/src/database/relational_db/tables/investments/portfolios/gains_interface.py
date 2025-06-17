from decimal import Decimal
from datetime import timedelta, date
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from domain.myfxbook import DayGain
from .daily_gains_table import DailyGain
from .portfolios_table import Portfolio


class GainsInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    @staticmethod
    def _gain_row(portfolio_id: int, gain: DayGain) -> dict:
        return dict(
            portfolio_id = portfolio_id,
            date = gain.date,
            gain_pct = gain.value,
            profit = gain.profit,
        )
        
    
    async def bulk_upsert_gains(self, rows: list[dict], chunk_size: int = 1000):
        if not rows:
            return
        for i in range(0, len(rows), chunk_size):
            batch = rows[i:i + chunk_size]
            query = insert(DailyGain).values(batch)
            query = query.on_conflict_do_update(
                index_elements=["portfolio_id", "date"],
                set_={
                    "gain_pct": query.excluded.gain_pct,
                    "profit": query.excluded.profit,
                },
            )
            await self.session.execute(query)
        
        
    async def fetch_sparklines(
        self, portfolios: list[Portfolio]
    ) -> dict[int, list[tuple[date, Decimal]]]:
        ids = [p.id for p in portfolios]
        
        query = (
            select(DailyGain.portfolio_id,
                DailyGain.date, DailyGain.gain_pct)
            .where(
                DailyGain.portfolio_id.in_(ids),
                DailyGain.date >= date.today() - timedelta(days=30)
            )
            .order_by(DailyGain.portfolio_id, DailyGain.date)
        )
        result = await self.session.execute(query)
        rows = result.all()

        spark_map: dict[int, list[tuple[date, Decimal]]] = {}
        for pid, _date, gain_pct in rows:
            spark_map.setdefault(pid, []).append({'date': _date, 'gain_percent': gain_pct})

        return spark_map
    
    
    async def gain_history(
        self, portfolio_id: int, days: int = 30
    ) -> list[dict[date, Decimal]] | list:
        query = (
            select(DailyGain.date, DailyGain.gain_pct)
            .where(
                DailyGain.portfolio_id == portfolio_id,
                DailyGain.date >= date.today() - timedelta(days=days)
            )
            .order_by(DailyGain.date)
        )
        result = await self.session.execute(query)
        rows = result.all()
        
        gains: list[dict[date, Decimal]] = []
        for _date, gain_pct in rows:
            gains.append({'date': _date, 'gain_percent': gain_pct})

        return gains
