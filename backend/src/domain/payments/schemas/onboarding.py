from pydantic import BaseModel, Field
from decimal import Decimal


class Onboarding(BaseModel):
    refresh_url: str = Field(...)
    return_url: str = Field(...)
