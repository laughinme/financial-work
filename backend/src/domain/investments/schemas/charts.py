from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date as dt_date


class SparklineGain(BaseModel):
    """Short gain values used for sparkline charts."""

    date: dt_date = Field(..., description="Date of the gain")
    gain_percent: Decimal = Field(..., description="Gain in percent for that day")
    # profit: Decimal
    
    
class BalanceEquity(BaseModel):
    """Daily balance and equity information."""

    date: dt_date = Field(..., description="Day")
    balance: Decimal = Field(..., description="Account balance")
    equity: Decimal = Field(..., description="Account equity")
    
    
class Drawdown(BaseModel):
    """Drawdown values over time."""

    date: dt_date = Field(..., description="Day")
    drawdown: Decimal = Field(..., description="Drawdown percentage")


class PortfolioCharts(BaseModel):
    """Aggregated chart data for a portfolio."""

    sparkline: list[SparklineGain] = Field(..., description="Gain sparkline data")
    balance_equity: list[BalanceEquity] = Field(..., description="Balance and equity history")
    drawdown: list[Drawdown] = Field(..., description="Drawdown history")
