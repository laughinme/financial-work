from pydantic import BaseModel, Field
from decimal import Decimal

from ...investments import OrderOut


class Settlement(BaseModel):
    """Portfolio settlement information."""
    
    portfolio_id: int = Field(..., description="Portfolio identifier")
    name: str = Field(..., description="Portfolio name")
    delta: Decimal = Field(..., description="Change since previous period")
    invest: Decimal = Field(..., description="Total invested")
    withdraw: Decimal = Field(..., description="Total withdrawn")
    orders: list[OrderOut] = Field(..., description="Orders included in settlement")
