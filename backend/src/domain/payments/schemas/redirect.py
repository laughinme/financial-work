from pydantic import BaseModel, Field

class RedirectPaymentSchema(BaseModel):
    url: str = Field(..., description="Redirect URL provided by payment provider")
