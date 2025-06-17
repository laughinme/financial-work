from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class AllocationPie(BaseModel):
    """Holdings allocations chart"""
    
    portfolio_id: int = Field(..., alias='id', description='Portfolio id')
    portfolio_name: str = Field(..., alias='name', description='Portfolio name')
    amount: Decimal = Field(..., alias='current_value', description='Absolute amount')
    share: Decimal = Field(..., description="User's holding share")
    percentage: Decimal = Field(..., description="User's share in percents")


class DailyPnl(BaseModel):
    date: datetime
    pnl: Decimal


class PortfolioValue(BaseModel):
    date: datetime
    equity: Decimal
    daily_pnl: Decimal | None = Field(
        None, description="Δ equity vs previous day (can be <0)"
    )
