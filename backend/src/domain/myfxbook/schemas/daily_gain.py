from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from decimal import Decimal

from .common import CommonModel


class DayGain(BaseModel):
    date: date
    value: Decimal
    profit: Decimal
    
    
    @field_validator('date', mode='before')
    @classmethod
    def transform_date(cls, v: str):
        return datetime.strptime(v, '%m/%d/%Y').date()


class DailyGainSchema(CommonModel):
    daily_gain: list[DayGain] = Field(..., alias='dailyGain')
    
    @field_validator('daily_gain', mode='before')
    @classmethod
    def remove_extra_nest(cls, v: list):
        if v == []:
            return v
        return [day[-1] for day in v]
