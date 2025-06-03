import uuid

from decimal import Decimal
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey, DECIMAL, UUID

from ...table_base import Base
from ...mixins import TimestampMixin


class UnitIssue(TimestampMixin, Base):
    __tablename__ = "unit_issue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='RESTRICT')
    )
    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('portfolios.id', ondelete='RESTRICT')
    )
    transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('transactions.id', ondelete='RESTRICT')
    )
    
    units: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False)
    price_at_issue: Mapped[Decimal] = mapped_column(DECIMAL(24, 8))
    
    user = relationship("User", back_populates="unit_issues")
    portfolio = relationship("Portfolio")
    transaction = relationship("Transaction", back_populates="unit_issues")
