from pydantic import BaseModel, Field
from decimal import Decimal


class AllocationPie(BaseModel):
    """Holdings allocations chart"""
    
    portfolio_id: int = Field(..., alias='id', description='Portfolio id')
    portfolio_name: str = Field(..., alias='name', description='Portfolio name')
    amount: Decimal = Field(..., alias='current_value', description='Absolute amount')
    share: Decimal = Field(..., description="User's holding share")
    percentage: Decimal = Field(..., description="User's share in percents")
