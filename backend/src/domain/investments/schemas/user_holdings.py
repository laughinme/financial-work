from pydantic import BaseModel, Field
from decimal import Decimal


class UserHolding(BaseModel):
    """Information about user portfolio holdings."""

    units: Decimal = Field(..., description="Units owned by the user")
    total_deposit: Decimal = Field(..., description="Total amount invested")
    total_withdraw: Decimal = Field(..., description="Total amount withdrawn")
    current_value: Decimal = Field(..., description="Current portfolio value")
    pnl: Decimal = Field(..., description="Total profit and loss")
