from pydantic import BaseModel, Field, field_validator
from decimal import Decimal


class InvestSchema(BaseModel):
    """Payload for creating an investment order."""

    amount: Decimal = Field(..., description="Amount of funds to invest")
    
    # currency: str = Field(..., max_length=3, min_length=3)

    # @field_validator('currency')
    # @classmethod
    # def verify_currency(cls, v: str):
    #     if v.upper() != 'USD': 
    #         raise ValueError('Only USD is allowed')
    #     return v.upper()
    
    
class WithdrawSchema(BaseModel):
    """Payload for withdrawing units from a portfolio."""

    units: Decimal = Field(..., description="Amount of units to withdraw")
