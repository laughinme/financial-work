from pydantic import BaseModel, Field
from decimal import Decimal


class InvestSchema(BaseModel):
    amount: Decimal = Field(...)
