from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime

from .common import CommonModel


class DayData(BaseModel):
    date: date
    balance: float
    pips: float
    lots: float
    floating_PL: float = Field(..., alias='floatingPL')
    profit: float
    growth_equity: float = Field(..., alias='growthEquity')
    floating_pips: float = Field(..., alias='floatingPips')
    
    
    @field_validator('date', mode='before')
    @classmethod
    def transform_date(cls, v: str):
        return datetime.strptime(v, '%m/%d/%Y').date()


class DataDailySchema(CommonModel):
    data_daily: list[list[DayData]] = Field(..., alias='dataDaily')
