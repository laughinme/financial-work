from typing import Annotated
from fastapi import Depends, Query

from core.security import auth_user, AuthRouter
from domain.users import CashFlow
from service.transactions import TransactionsService, get_transactions_service
from database.relational_db import User


router = AuthRouter()


@router.get(
    path='/cashflow',
    response_model=list[CashFlow]
)
async def cashflow(
    service: Annotated[TransactionsService, Depends(get_transactions_service)],
    user: Annotated[User, Depends(auth_user)],
    days: int = Query(90, ge=1, le=365, description='Chart chronological period'),
):
    return await service.cashflow(user.id, days)
