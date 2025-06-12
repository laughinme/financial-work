import uuid

from decimal import Decimal
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey, DECIMAL, UUID, PrimaryKeyConstraint

from ...table_base import Base
from ...mixins import TimestampMixin


class Holding(Base, TimestampMixin):
    __tablename__ = "holdings"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='RESTRICT'), primary_key=True
    )
    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('portfolios.id', ondelete='RESTRICT'), primary_key=True
    )

    units: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False)
    total_deposit: Mapped[Decimal] = mapped_column(DECIMAL(18, 8), nullable=False)
    total_withdraw: Mapped[Decimal] = mapped_column(DECIMAL(18, 8), nullable=False, default=Decimal('0'))
    current_value: Mapped[Decimal] = mapped_column(DECIMAL(18, 8), nullable=False)
    pnl: Mapped[Decimal] = mapped_column(DECIMAL(18, 8), nullable=False, default=Decimal('0'))
    
    __table_args__ = (
        PrimaryKeyConstraint('portfolio_id', 'user_id', name='pk_portfolio_user'),
    )
    
    portfolio = relationship("Portfolio", back_populates="holdings")
    user = relationship("User", back_populates="holdings")
