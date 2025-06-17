from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from decimal import Decimal

from .common import CommonModel


class DayData(BaseModel):
    date: date
    balance: Decimal
    pips: Decimal
    lots: Decimal
    floating_PL: Decimal = Field(..., alias='floatingPL')
    profit: Decimal
    growth_equity: Decimal = Field(..., alias='growthEquity')
    floating_pips: Decimal = Field(..., alias='floatingPips')
    deposit: Decimal | None = None
    withdrawal: Decimal | None = None
    
    
    @field_validator('date', mode='before')
    @classmethod
    def transform_date(cls, v: str):
        return datetime.strptime(v, '%m/%d/%Y').date()


class DataDailySchema(CommonModel):
    data_daily: list[DayData] = Field(..., alias='dataDaily')
    
    @field_validator('data_daily', mode='before')
    @classmethod
    def remove_extra_nest(cls, v: list):
        if v == []:
            return v
        return [day[-1] for day in v]
