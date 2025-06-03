from pydantic import BaseModel

class RedirectPaymentSchema(BaseModel):
    url: str