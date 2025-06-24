from fastapi import Depends, Query

from core.security import auth_user, AuthRouter
from service.transactions import TransactionsService, get_transactions_service
from database.relational_db import User
from domain.payments import TransactionBrief


router = AuthRouter()


@router.get(
    '/',
    response_model=list[TransactionBrief]
)
async def list_transactions(
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    service: TransactionsService = Depends(get_transactions_service),
    user: User = Depends(auth_user)
):
    return await service.list_user(user.id, size, page)
