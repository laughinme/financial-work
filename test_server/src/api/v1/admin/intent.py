from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime, UTC
from decimal import Decimal

from domain.myfxbook import STATE
from service.myfx_service import MyFXService, get_myfxservice

router = APIRouter()


class AdminPayload(BaseModel):
    portfolio_id: int
    deposits: Decimal
    withdrawals: Decimal
    

@router.post(
    path='/admin/invest'
)
async def admin_invest(
    payload: AdminPayload,
    svc: Annotated[MyFXService, Depends(get_myfxservice)]
):
    p = STATE[payload.portfolio_id]
    p.deposits += payload.deposits
    p.withdrawals += payload.withdrawals
    p.balance += payload.deposits - payload.withdrawals
    p.equity += payload.deposits - payload.withdrawals
    p.last_update_date = datetime.now(UTC)
    
    svc.upsert_today_record(p, payload.deposits, payload.withdrawals)
