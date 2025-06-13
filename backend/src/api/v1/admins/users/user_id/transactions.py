from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path

from core.security import auth_user, auth_admin
from service.transactions import TransactionsService, get_transactions_service
from database.relational_db import User
from domain.payments import TransactionBrief


router = APIRouter()

@router.get(
    '/transactions',
    response_model=list[TransactionBrief]
)
async def user_transactions(
    user_id: Annotated[UUID, Path(..., description='User id')],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    service: TransactionsService = Depends(get_transactions_service),
    _: User = Depends(auth_admin)
):
    return await service.list_user(user_id, size, page)
