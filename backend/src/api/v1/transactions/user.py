from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path, HTTPException

from core.security import auth_user
from service.transactions import TransactionsService, get_transactions_service
from database.relational_db import User
from domain.payments import TransactionBrief, TransactionFull


router = APIRouter()


@router.get('/', response_model=list[TransactionBrief])
async def list_transactions(
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    service: TransactionsService = Depends(get_transactions_service),
    user: User = Depends(auth_user)
):
    return await service.list_user(user.id, size, page)


@router.get('/{tx_id}', response_model=TransactionFull)
async def transaction_detail(
    tx_id: Annotated[int, Path(..., description='Transaction id')],
    service: TransactionsService = Depends(get_transactions_service),
    user: User = Depends(auth_user)
):
    tx = await service.get_by_id(tx_id, user.id)
    if tx is None:
        raise HTTPException(404, detail='Transaction not found')
    return tx
