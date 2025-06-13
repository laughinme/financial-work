import uuid

from decimal import Decimal
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, UUID, DECIMAL, Enum, CHAR, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from domain.payments import PaymentStatus, PaymentProvider
from ...table_base import Base
from ...mixins import TimestampMixin


class PaymentIntent(TimestampMixin, Base):
    __tablename__ = "payment_intents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT")
    )
    provider_payment_id: Mapped[str] = mapped_column(String, nullable=True)
    
    amount: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), nullable=False, index=True)
    provider: Mapped[PaymentProvider] = mapped_column(Enum(PaymentProvider), nullable=False)
    _metadata: Mapped[str] = mapped_column(JSONB, nullable=True)
    
    __table_args__ = (
        UniqueConstraint('provider', 'provider_payment_id', name='uq_payment_provider_id'),
    )
    
    transactions = relationship("Transaction", back_populates="intent", lazy="selectin")
