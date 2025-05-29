from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime

from .common import CommonModel


class DayGain(BaseModel):
    date: date
    value: float
    profit: float
    
    
    @field_validator('date', mode='before')
    @classmethod
    def transform_date(cls, v: str):
        return datetime.strptime(v, '%m/%d/%Y').date()


class DailyGainSchema(CommonModel):
    daily_gain: list[list[DayGain]] = Field(..., alias='dailyGain')
