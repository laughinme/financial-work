import uuid

from decimal import Decimal
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey, UUID, DECIMAL, Enum

from domain.payments import TransactionType
from ...table_base import Base
from ...mixins import TimestampMixin


class Transaction(TimestampMixin, Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    intent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('payment_intents.id', ondelete='RESTRICT'), nullable=True
    )
    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('portfolios.id', ondelete='RESTRICT'), nullable=True
    )
    
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    comment: Mapped[str] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="transactions")
    portfolio = relationship("Portfolio", back_populates="transactions")
    intent = relationship("PaymentIntent", back_populates="transactions")
    unit_issues = relationship("UnitIssue", back_populates="transaction")
