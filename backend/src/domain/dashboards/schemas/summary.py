from pydantic import BaseModel, Field
from decimal import Decimal


class DashboardSchema(BaseModel):
    total_equity: Decimal
    total_pnl: Decimal
    today_pnl: Decimal
    portfolios_num: Decimal
    # last_sync: Decimal
