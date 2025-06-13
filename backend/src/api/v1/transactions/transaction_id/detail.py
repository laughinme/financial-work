from typing import Annotated

from fastapi import Depends, Path, HTTPException

from core.security import auth_user, AuthRouter
from service.transactions import TransactionsService, get_transactions_service
from database.relational_db import User
from domain.payments import TransactionFull


router = AuthRouter()


@router.get(
    '/', 
    response_model=TransactionFull,
    responses={
        404: {"description": "Transaction not found"}
    }
)
async def transaction_detail(
    transaction_id: Annotated[int, Path(..., description='Transaction id')],
    service: TransactionsService = Depends(get_transactions_service),
    user: User = Depends(auth_user)
):
    transaction = await service.get_by_id(transaction_id, user.id)
    if transaction is None:
        raise HTTPException(404, detail='Transaction not found')
    
    return transaction
