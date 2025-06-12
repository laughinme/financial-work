from decimal import Decimal
from datetime import date as dtm_date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey, DECIMAL, Date

from ...table_base import Base
from ...mixins import TimestampMixin


class DailyGain(TimestampMixin, Base):
    __tablename__ = "daily_gains"

    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('portfolios.id', ondelete='RESTRICT'), primary_key=True
    )
    
    date: Mapped[dtm_date] = mapped_column(Date, primary_key=True)
    gain_pct: Mapped[Decimal] = mapped_column(DECIMAL(7, 3), nullable=False)
    profit: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)

    portfolio = relationship('Portfolio', back_populates='gains')
