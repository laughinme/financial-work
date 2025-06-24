from pydantic import BaseModel, Field
from datetime import datetime


class RedirectPaymentSchema(BaseModel):
    url: str = Field(..., description="Redirect URL provided by stripe")


class StripeAccountLink(BaseModel):
    created_at: datetime = Field(..., alias='created')
    expires_at: datetime = Field(...)
    url: str = Field(..., description='AccountLink url')
