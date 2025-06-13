import uuid

from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, UUID, DECIMAL, CHAR, Integer, DateTime
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

from domain.payments import PaymentStatus, TransferMethod, TransferDirection
from ...table_base import Base
from ...mixins import TimestampMixin


class AdminTransfer(TimestampMixin, Base):
    __tablename__ = "admin_transfers"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT")
    )
    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('portfolios.id', ondelete='RESTRICT')
    )
    stripe_session_id: Mapped[str] = mapped_column(String, nullable=True)
    
    direction: Mapped[TransferDirection] = mapped_column(PGEnum(TransferDirection), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    method: Mapped[TransferMethod] = mapped_column(PGEnum(TransferMethod), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(PGEnum(PaymentStatus), nullable=False, index=True)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
