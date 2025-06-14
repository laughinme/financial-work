from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from ..enums import TransactionType


class TransactionBrief(BaseModel):
    """Short information about a transaction."""

    id: int = Field(..., description="Transaction identifier")
    portfolio_id: int | None = Field(None, description="Related portfolio id")
    intent_id: UUID | None = Field(None, description="Payment intent id")
    type: TransactionType = Field(..., description="Type of the transaction")
    amount: Decimal = Field(..., description="Transaction amount")
    currency: str = Field(..., description="Currency code")
    comment: str | None = Field(None, description="Additional comment")
    created_at: datetime = Field(..., description="Creation timestamp")


class TransactionFull(TransactionBrief):
    """Full transaction information including owner."""

    user_id: UUID = Field(..., description="User identifier")
    updated_at: datetime | None = Field(None, description="Last update time")
