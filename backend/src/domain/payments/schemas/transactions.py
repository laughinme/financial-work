from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from ..enums import TransactionType


class TransactionBrief(BaseModel):
    id: int
    portfolio_id: int | None = None
    intent_id: UUID | None = None
    type: TransactionType
    amount: Decimal
    currency: str
    comment: str | None = None
    created_at: datetime


class TransactionFull(TransactionBrief):
    user_id: UUID
    updated_at: datetime | None = None
