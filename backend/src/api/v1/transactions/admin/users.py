from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path

from core.security import auth_user
from service.transactions import TransactionsService, get_transactions_service
from database.relational_db import User
from domain.payments import TransactionBrief

router = APIRouter(prefix='/users')


@router.get('/{user_id}/transactions', response_model=list[TransactionBrief])
async def user_transactions(
    user_id: Annotated[UUID, Path(..., description='User id')],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    service: TransactionsService = Depends(get_transactions_service),
    _: User = Depends(auth_user)
):
    return await service.list_for_user(user_id, size, page)
