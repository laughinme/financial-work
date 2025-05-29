from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from .common import CommonModel


class ServerSchema(BaseModel):
    name: str


class AccountSchema(BaseModel):
    id: int
    name: str
    description: str | None = Field(None)
    account_id: int = Field(..., alias='accountId')
    gain: float
    abs_gain: float = Field(..., alias='absGain')
    daily: float
    monthly: float
    withdrawals: int
    deposits: float
    interest: float
    profit: float
    balance: float
    drawdown: float
    equity: float
    equity_percent: float = Field(..., alias='equityPercent')
    demo: bool
    last_update_date: datetime = Field(..., alias='lastUpdateDate')
    creation_date: datetime = Field(..., alias='creationDate')
    first_trade_date: datetime = Field(..., alias='firstTradeDate')
    tracking: float
    views: float
    commission: float
    currency: str
    profit_factor: float = Field(..., alias='profitFactor')
    pips: float
    portfolio: str
    invitation_url: str = Field(..., alias='invitationUrl')
    server: ServerSchema
    
    
    @field_validator('last_update_date', 'creation_date', 'first_trade_date', mode='before')
    @classmethod
    def transform_to_datetime(cls, v: str):
        return datetime.strptime(v, "%m/%d/%Y %H:%M")


class AccountsSchema(CommonModel):
    accounts: list[AccountSchema]
