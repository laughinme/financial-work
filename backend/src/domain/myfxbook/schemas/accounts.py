from pydantic import BaseModel, Field, field_validator
from datetime import datetime, UTC
from decimal import Decimal

from .common import CommonModel


class ServerSchema(BaseModel):
    name: str = Field(..., description="Server name")


class AccountSchema(BaseModel):
    """Detailed account information returned by MyFXbook."""

    id: int = Field(..., description="Internal MyFXbook account id")
    name: str = Field(..., description="Account name")
    description: str | None = Field(None, description="Account description")
    account_id: int = Field(..., alias='accountId', description="Broker account id")
    gain: Decimal = Field(..., description="Gain in percent")
    abs_gain: Decimal = Field(..., alias='absGain', description="Absolute gain in percent")
    daily: Decimal = Field(..., description="Daily performance")
    monthly: Decimal = Field(..., description="Monthly performance")
    withdrawals: Decimal = Field(..., description="Number of withdrawals")
    deposits: Decimal = Field(..., description="Total deposits")
    interest: Decimal = Field(..., description="Interest received")
    profit: Decimal = Field(..., description="Total profit")
    balance: Decimal = Field(..., description="Account balance")
    drawdown: Decimal = Field(..., description="Drawdown percentage")
    equity: Decimal = Field(..., description="Account equity")
    equity_percent: Decimal = Field(..., alias='equityPercent', description="Equity percent")
    demo: bool = Field(..., description="Is demo account")
    last_update_date: datetime = Field(..., alias='lastUpdateDate', description="Last update time")
    creation_date: datetime = Field(..., alias='creationDate', description="Account creation time")
    first_trade_date: datetime = Field(..., alias='firstTradeDate', description="Date of first trade")
    tracking: Decimal = Field(..., description="Tracking value")
    views: Decimal = Field(..., description="Number of views")
    commission: Decimal = Field(..., description="Commissions paid")
    currency: str = Field(..., description="Account currency")
    profit_factor: Decimal = Field(..., alias='profitFactor', description="Profit factor")
    pips: Decimal = Field(..., description="Accumulated pips")
    portfolio: str = Field(..., description="Portfolio name")
    invitation_url: str = Field(..., alias='invitationUrl', description="Invitation link")
    server: ServerSchema = Field(..., description="Trading server info")
    
    
    @field_validator('last_update_date', 'creation_date', 'first_trade_date', mode='before')
    @classmethod
    def transform_to_datetime(cls, v: str):
        naive = datetime.strptime(v, "%m/%d/%Y %H:%M")
        return naive.replace(tzinfo=UTC)


class AccountsSchema(CommonModel):
    accounts: list[AccountSchema]
