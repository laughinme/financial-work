import uuid

from decimal import Decimal
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey, DECIMAL, UUID, CHAR, Enum
# from sqlalchemy.dialects.postgresql import ENUM as PGEnum

from domain.investments import InvestOrderStatus, OrderDirection
from ...table_base import Base
from ...mixins import TimestampMixin


class InvestOrder(Base, TimestampMixin):
    __tablename__ = "invest_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='RESTRICT')
    )
    portfolio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('portfolios.id', ondelete='RESTRICT')
    )

    direction: Mapped[OrderDirection] = mapped_column(Enum(OrderDirection), nullable=False)
    
    amount: Mapped[Decimal] = mapped_column(DECIMAL(24, 8), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    status: Mapped[InvestOrderStatus] = mapped_column(Enum(InvestOrderStatus), nullable=False)

    # TODO: add relationships
