from typing import Annotated
from fastapi import Depends

from core.security import auth_user, AuthRouter
from domain.payments import WalletSchema
from service.transactions import TransactionsService, get_transactions_service
from database.relational_db import User


router = AuthRouter()

@router.get(
    path="/balance",
    response_model=WalletSchema,
    status_code=200
)
async def balance(
    service: Annotated[TransactionsService, Depends(get_transactions_service)],
    user: Annotated[User, Depends(auth_user)]
):
    wallet = await service.balance(user.id)
    return wallet
