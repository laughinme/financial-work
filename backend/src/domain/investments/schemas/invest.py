from pydantic import BaseModel, Field, field_validator
from decimal import Decimal


class InvestSchema(BaseModel):
    amount: Decimal = Field(...)
    
    # currency: str = Field(..., max_length=3, min_length=3)

    # @field_validator('currency')
    # @classmethod
    # def verify_currency(cls, v: str):
    #     return v.upper()
