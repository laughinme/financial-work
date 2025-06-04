import uuid

from decimal import Decimal
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, UUID, DECIMAL, CHAR, PrimaryKeyConstraint

from ...table_base import Base
# from ...mixins import TimestampMixin


class Wallet(Base):
    __tablename__ = "wallets"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='RESTRICT'), primary_key=True
    )
    
    currency: Mapped[str] = mapped_column(CHAR(3), primary_key=True)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(18,2), default=Decimal('0'), nullable=False)
    locked: Mapped[Decimal] = mapped_column(DECIMAL(18,2), default=Decimal('0'), nullable=False)
    
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'currency', name='pk_userid_currency'),
    )

    user = relationship('User', back_populates='wallets')
