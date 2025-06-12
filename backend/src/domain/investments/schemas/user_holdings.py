from pydantic import BaseModel, Field
from decimal import Decimal


class UserHolding(BaseModel):
    units: Decimal
    total_deposit: Decimal
    total_withdraw: Decimal
    current_value: Decimal
    pnl: Decimal
