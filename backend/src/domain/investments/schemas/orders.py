from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ...investments import OrderDirection, InvestOrderStatus


class OrderOut(BaseModel):
    id: int
    user_id: UUID
    portfolio_id: int
    direction: OrderDirection
    amount: Decimal
    status: InvestOrderStatus
    created_at: datetime
