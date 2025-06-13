from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ...investments import OrderDirection, InvestOrderStatus


class OrderOut(BaseModel):
    """Information about an investment order."""

    id: int = Field(..., description="Order identifier")
    user_id: UUID = Field(..., description="Identifier of the owner")
    portfolio_id: int = Field(..., description="Related portfolio id")
    direction: OrderDirection = Field(..., description="Order type")
    amount: Decimal = Field(..., description="Order amount")
    status: InvestOrderStatus = Field(..., description="Current order status")
    created_at: datetime = Field(..., description="Creation timestamp")
