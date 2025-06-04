from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

from .charts import SparklineGain
from ..enums import RiskScale


class PortfolioPreview(BaseModel):
    id: int
    name: str
    description: str | None = None
    broker: str
    currency: str
    risk: RiskScale | None = None
    nav_price: Decimal
    balance: Decimal
    equity: Decimal
    drawdown: Decimal
    
    gain_percent: Decimal
    net_profit: Decimal
    first_trade_at: datetime
    
    deposit: Decimal
    holders: int = Field(..., title='Number of investors to this portfolio')
    duration: int
    
    sparkline_gain: list[SparklineGain] = []


class PortfolioOverview(BaseModel):
    id: int
    name: str
    description: str | None = None
    broker: str
    currency: str
    risk: RiskScale | None = None
    nav_price: Decimal
    balance: Decimal
    equity: Decimal
    drawdown: Decimal
    
    gain_percent: Decimal
    net_profit: Decimal
    first_trade_at: datetime
    
    deposit: Decimal
    holders: int = Field(..., title='Number of investors to this portfolio')
    duration: int
