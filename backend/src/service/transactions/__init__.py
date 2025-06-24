from fastapi import Depends

from database.relational_db import UoW, get_uow, TransactionInterface, WalletInterface
from .transactions_service import TransactionsService


async def get_transactions_service(
    uow: UoW = Depends(get_uow),
) -> TransactionsService:
    tx_repo = TransactionInterface(uow.session)
    w_repo = WalletInterface(uow.session)
    return TransactionsService(uow, tx_repo, w_repo)
