from pydantic import BaseModel
from decimal import Decimal

from ...investments import OrderOut


class Settlement(BaseModel):
    portfolio_id: int
    name: str
    delta: Decimal
    invest: Decimal
    withdraw: Decimal
    orders: list[OrderOut]
