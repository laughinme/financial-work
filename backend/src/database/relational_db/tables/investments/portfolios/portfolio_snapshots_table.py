from decimal import Decimal
from datetime import date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey, DECIMAL, Date, PrimaryKeyConstraint, Index

from ...table_base import Base
from ...mixins import TimestampMixin


class PortfolioSnapshot(TimestampMixin, Base):
    __tablename__ = "portfolio_snapshots"

    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('portfolios.id', ondelete='RESTRICT'), primary_key=True
    )
    snapshot_date: Mapped[date] = mapped_column(
        Date, nullable=False, default=date.today(), primary_key=True
    )
    
    nav_price: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(24, 2), nullable=False)
    equity: Mapped[Decimal] = mapped_column(DECIMAL(24, 2), nullable=False)
    drawdown: Mapped[Decimal] = mapped_column(DECIMAL(7, 3), nullable=False)   # %
    
    __table_args__ = (
        PrimaryKeyConstraint('portfolio_id', 'snapshot_date', name='pk_portfolio_snapshot'),
        Index('ix_snap_portfolio_date', 'portfolio_id', 'snapshot_date'),
    )
    
    portfolio = relationship("Portfolio", back_populates="snapshots")
