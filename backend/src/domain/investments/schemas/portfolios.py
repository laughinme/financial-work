from pydantic import BaseModel, Field


class PortfolioSchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    broker: str
    currency: str
    risk: str
    
    