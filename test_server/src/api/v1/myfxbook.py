from typing import Annotated
from fastapi import APIRouter, Query, Depends
from datetime import date
from decimal import Decimal

from domain.myfxbook import STATE
from service.myfx_service import MyFXService, get_myfxservice


router = APIRouter()


@router.get('/get-my-accounts.json')
async def get_my_accounts(
    svc: Annotated[MyFXService, Depends(get_myfxservice)],
    session: str = Query(...),
):
    accounts = [svc.convert_state_to_account(p) for p in STATE.values()]
    return {"error": False, "message": "", "accounts": accounts}


@router.get('/get-data-daily.json')
async def get_data_daily(
    svc: Annotated[MyFXService, Depends(get_myfxservice)],
    session: str = Query(...),
    id: int = Query(...),
    start: date = Query(...),
    end: date = Query(...)
):
    p = STATE[id]
    data = [
        svc.convert_day_record(r) 
        for d, r in sorted(p.history.items()) 
        if start <= d <= end
    ]
    return {"error": False, "message": "", "dataDaily": data}

@router.get('/get-daily-gain.json')
async def get_daily_gain(
    svc: Annotated[MyFXService, Depends(get_myfxservice)],
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
            data.append(svc.convert_day_gain(r, previous_equity))
            previous_equity = r.equity
    return {"error": False, "message": "", "dailyGain": data}
