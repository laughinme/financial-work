from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date


class SparklineGain(BaseModel):
    date: date
    gain_percent: Decimal
    # profit: Decimal
    
    
class BalanceEquity(BaseModel):
    date: date
    balance: Decimal
    equity: Decimal
    
    
class Drawdown(BaseModel):
    date: date
    drawdown: Decimal


class PortfolioCharts(BaseModel):
    sparkline: list[SparklineGain]
    balance_equity: list[BalanceEquity]
    drawdown: list[Drawdown]
