from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

from domain.myfxbook import (
    convert_state_to_account,
    convert_day_record,
    convert_day_gain,
    upsert_today_record,
    seed_history,
    STATE,
    PortfolioState
)

router = APIRouter()

# Seed default state on module import
if not STATE:
    p = PortfolioState(id=1, balance=Decimal('0'), equity=Decimal('0'), deposits=Decimal('0'), withdrawals=Decimal('0'))
    seed_history(p)
    STATE[p.id] = p

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
    data = [convert_day_gain(r, p.initial_equity) for d, r in sorted(p.history.items()) if start <= d <= end]
    return {"error": False, "message": "", "dailyGain": data}

class AdminBody(BaseModel):
    pid: int
    amount: Decimal

@router.get('/admin/deposit')
async def admin_deposit(body: AdminBody):
    p = STATE[body.pid]
    p.deposits += body.amount
    p.balance += body.amount
    p.equity += body.amount
    upsert_today_record(p)
    return {"ok": True}

@router.get('/admin/withdraw')
async def admin_withdraw(body: AdminBody):
    p = STATE[body.pid]
    p.withdrawals += body.amount
    p.balance -= body.amount
    p.equity -= body.amount
    upsert_today_record(p)
    return {"ok": True}
