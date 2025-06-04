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
    

# class PortfolioCharts(BaseModel):
#     sparkline: list[tuple[date, Decimal]] = Field(
#         [], description='Data for sparkline gain: [date, gain %]'
#     )
#     balance_equity: list[tuple[date, Decimal, Decimal]] = Field(
#         [], description='Data for balance_equity chart: [date, balance, equity]'
#     )
#     drawdown: list[tuple[date, Decimal]] = Field(
#         [], description='Data for drawdown chart: [date, drawdown %]'
#     )
