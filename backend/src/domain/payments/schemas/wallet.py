from pydantic import BaseModel, Field
from decimal import Decimal


class WalletSchema(BaseModel):
    currency: str = Field(
        ..., max_length=3, min_length=3, description="Three letter ISO wallet currency code in uppercase"
    )
    balance: Decimal = Field(..., description="Available balance")
    locked: Decimal = Field(..., description="Locked balance")
