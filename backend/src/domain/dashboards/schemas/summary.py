from pydantic import BaseModel, Field
from decimal import Decimal


class DashboardSchema(BaseModel):
    """Aggregated information about user's portfolios."""

    total_equity: Decimal = Field(..., description="Total equity of all portfolios")
    total_pnl: Decimal = Field(..., description="Total profit and loss")
    today_pnl: Decimal = Field(..., description="Today's profit and loss")
    portfolios_num: Decimal = Field(..., description="Number of portfolios owned")
    # last_sync: Decimal
