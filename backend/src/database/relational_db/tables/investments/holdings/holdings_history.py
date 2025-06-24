import uuid

from decimal import Decimal
from datetime import date as date_
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey, DECIMAL, UUID, UniqueConstraint, Date

from ...table_base import Base
from ...mixins import TimestampMixin


class HoldingHistory(Base, TimestampMixin):
    __tablename__ = "holdings_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='RESTRICT')
    )
    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('portfolios.id', ondelete='RESTRICT')
    )
    date: Mapped[date_] = mapped_column(Date, nullable=False)

    units: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False)
    total_deposit: Mapped[Decimal] = mapped_column(DECIMAL(18, 8), nullable=False)
    total_withdraw: Mapped[Decimal] = mapped_column(DECIMAL(18, 8), nullable=False)
    current_value: Mapped[Decimal] = mapped_column(DECIMAL(18, 8), nullable=False)
    pnl: Mapped[Decimal] = mapped_column(DECIMAL(18, 8), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'portfolio_id', 'date', name='uq_holding_history'),
    )
