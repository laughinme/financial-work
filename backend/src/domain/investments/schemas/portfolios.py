from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

from .charts import SparklineGain
from ..enums import RiskScale


class PortfolioPreview(BaseModel):
    """Short information about a portfolio shown in lists."""

    id: int = Field(..., description="Portfolio identifier")
    name: str = Field(..., description="Portfolio name")
    description: str | None = Field(None, description="Optional portfolio description")
    broker: str = Field(..., description="Broker name")
    currency: str = Field(..., description="Portfolio currency")
    risk: RiskScale | None = Field(None, description="Risk level of the portfolio")
    nav_price: Decimal = Field(..., description="Current NAV price")
    balance: Decimal = Field(..., description="Account balance")
    equity: Decimal = Field(..., description="Account equity")
    drawdown: Decimal = Field(..., description="Current drawdown in percent")
    
    gain_percent: Decimal = Field(..., description="Total gain in percent")
    net_profit: Decimal = Field(..., description="Net profit amount")
    first_trade_at: datetime = Field(..., description="Date of the first trade")
    
    deposit: Decimal = Field(..., description="Total amount deposited")
    holders: int = Field(..., description="Number of investors to this portfolio")
    duration: int = Field(..., description="Portfolio lifetime in days")
    
    invested_by_user: bool = Field(..., description="Shows if current user invested")
    
    sparkline_gain: list[SparklineGain] = Field(default_factory=list, description="Sparkline data for gains")


class PortfolioOverview(BaseModel):
    """Detailed information about a specific portfolio."""

    id: int = Field(..., description="Portfolio identifier")
    name: str = Field(..., description="Portfolio name")
    description: str | None = Field(None, description="Optional portfolio description")
    broker: str = Field(..., description="Broker name")
    currency: str = Field(..., description="Portfolio currency")
    risk: RiskScale | None = Field(None, description="Risk level of the portfolio")
    nav_price: Decimal = Field(..., description="Current NAV price")
    balance: Decimal = Field(..., description="Account balance")
    equity: Decimal = Field(..., description="Account equity")
    drawdown: Decimal = Field(..., description="Current drawdown in percent")
    
    gain_percent: Decimal = Field(..., description="Total gain in percent")
    net_profit: Decimal = Field(..., description="Net profit amount")
    first_trade_at: datetime = Field(..., description="Date of the first trade")
    
    deposit: Decimal = Field(..., description="Total amount deposited")
    holders: int = Field(..., description="Number of investors to this portfolio")
    duration: int = Field(..., description="Portfolio lifetime in days")
    
    invested_by_user: bool = Field(..., description="Shows if current user invested")
