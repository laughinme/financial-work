from pydantic import BaseModel, Field, field_validator
from datetime import datetime, UTC
from decimal import Decimal

from .common import CommonModel


class ServerSchema(BaseModel):
    name: str


class AccountSchema(BaseModel):
    id: int
    name: str
    description: str | None = Field(None)
    account_id: int = Field(..., alias='accountId')
    gain: Decimal
    abs_gain: Decimal = Field(..., alias='absGain')
    daily: Decimal
    monthly: Decimal
    withdrawals: int
    deposits: Decimal
    interest: Decimal
    profit: Decimal
    balance: Decimal
    drawdown: Decimal
    equity: Decimal
    equity_percent: Decimal = Field(..., alias='equityPercent')
    demo: bool
    last_update_date: datetime = Field(..., alias='lastUpdateDate')
    creation_date: datetime = Field(..., alias='creationDate')
    first_trade_date: datetime = Field(..., alias='firstTradeDate')
    tracking: Decimal
    views: Decimal
    commission: Decimal
    currency: str
    profit_factor: Decimal = Field(..., alias='profitFactor')
    pips: Decimal
    portfolio: str
    invitation_url: str = Field(..., alias='invitationUrl')
    server: ServerSchema
    
    
    @field_validator('last_update_date', 'creation_date', 'first_trade_date', mode='before')
    @classmethod
    def transform_to_datetime(cls, v: str):
        naive = datetime.strptime(v, "%m/%d/%Y %H:%M")
        return naive.replace(tzinfo=UTC)


class AccountsSchema(CommonModel):
    accounts: list[AccountSchema]
