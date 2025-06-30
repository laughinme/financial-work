from typing import Annotated
from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime, date, UTC
from decimal import Decimal

from domain.myfxbook import (
    convert_state_to_account,
    convert_day_record,
    convert_day_gain,
    upsert_today_record,
    seed_portfolios,
    STATE
)


router = APIRouter()

# Seed default state on module import
if not STATE:
    seed_portfolios(5)
    
    
@router.get('/login.json')
async def login(email: str = Query(...), password: str = Query(...)):
    return {"error": False, "message": "", "session": "session_123"}

@router.get('/logout.json')
async def logout(session: str = Query(...)):
    return {"error": False, "message": "ok"}


@router.get('/get-my-accounts.json')
async def get_my_accounts(session: str = Query(...)):
    accounts = [convert_state_to_account(p) for p in STATE.values()]
    return {"error": False, "message": "", "accounts": accounts}


@router.get('/get-data-daily.json')
async def get_data_daily(
    session: str = Query(...),
    id: int = Query(...),
    start: date = Query(...),
    end: date = Query(...)
):
    p = STATE[id]
    data = [convert_day_record(r) for d, r in sorted(p.history.items()) if start <= d <= end]
    return {"error": False, "message": "", "dataDaily": data}

@router.get('/get-daily-gain.json')
async def get_daily_gain(
    session: str = Query(...),
    id: int = Query(...),
    start: date = Query(...),
    end: date = Query(...)
):
    p = STATE[id]
    
    previous_equity = Decimal('0')
    data = []
    for d, r in sorted(p.history.items()):
        if start <= d <= end:
            data.append(convert_day_gain(r, previous_equity))
            previous_equity = r.equity
    return {"error": False, "message": "", "dailyGain": data}

class AdminPayload(BaseModel):
    portfolio_id: int
    deposits: Decimal
    withdrawals: Decimal
    

@router.post(
    path='/admin/invest'
)
async def admin_invest(
    payload: AdminPayload
):
    p = STATE[payload.portfolio_id]
    p.deposits += payload.deposits
    p.withdrawals += payload.withdrawals
    p.balance += payload.deposits - payload.withdrawals
    p.equity += payload.deposits - payload.withdrawals
    p.last_update_date = datetime.now(UTC)
    
    upsert_today_record(p, payload.deposits, payload.withdrawals)
