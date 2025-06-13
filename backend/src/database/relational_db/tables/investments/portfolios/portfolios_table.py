from decimal import Decimal
from datetime import datetime, UTC
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, DECIMAL, Enum, DateTime, CHAR, Boolean

from domain.investments import RiskScale
from ...table_base import Base
from ...mixins import TimestampMixin


class Portfolio(TimestampMixin, Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    oid_myfx: Mapped[int] = mapped_column(Integer, nullable=False, index=True, unique=True)
    account_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    broker: Mapped[str] = mapped_column(String, nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    
    risk: Mapped[RiskScale] = mapped_column(Enum(RiskScale), nullable=True)
    
    units_total: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False, default=Decimal('0'))
    nav_price: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False, default=Decimal('1'))
    balance: Mapped[Decimal] = mapped_column(DECIMAL(24, 2), nullable=False)
    equity: Mapped[Decimal] = mapped_column(DECIMAL(24, 2), nullable=False)
    drawdown: Mapped[Decimal] = mapped_column(DECIMAL(6, 3), nullable=False) # in percent
    
    deposits: Mapped[Decimal] = mapped_column(DECIMAL(24, 2), nullable=False)
    withdrawals: Mapped[Decimal] = mapped_column(DECIMAL(24, 2), nullable=False)
    invitation_url: Mapped[str] = mapped_column(String, nullable=True)
    
    gain_percent: Mapped[Decimal] = mapped_column(DECIMAL(9, 3), nullable=False) # net % gain
    net_profit: Mapped[Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)
    
    first_trade_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_sync: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now(UTC)
    )
    last_update_myfx: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    transactions = relationship("Transaction", back_populates="portfolio", lazy="noload")
    holdings = relationship("Holding", back_populates="portfolio", lazy="selectin")
    snapshots = relationship(
        "PortfolioSnapshot", 
        back_populates="portfolio", 
        order_by="PortfolioSnapshot.snapshot_date.desc()"
    )
    gains = relationship(
        "DailyGain", 
        back_populates='portfolio',
        order_by="DailyGain.date.desc()"
    )
