from pydantic import BaseModel
from decimal import Decimal


class AdminPayload(BaseModel):
    portfolio_id: int
    deposits: Decimal
    withdrawals: Decimal
