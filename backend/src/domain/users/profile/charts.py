from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class CashFlow(BaseModel):
    date: datetime
    deposit: Decimal = Field(
        ..., alias="deposits", description='Sum of deposits for current date'
    )
    withdraw: Decimal = Field(
        ..., alias="withdrawals", description='Sum of withdrawals for current date'
    )
