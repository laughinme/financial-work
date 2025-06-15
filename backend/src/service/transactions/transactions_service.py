from uuid import UUID

from database.relational_db import (
    UoW, TransactionInterface, Transaction, WalletInterface, Wallet
)


class TransactionsService:
    def __init__(
        self,
        uow: UoW,
        t_repo: TransactionInterface,
        w_repo: WalletInterface
        
    ):
        self.uow = uow
        self.t_repo = t_repo
        self.w_repo = w_repo


    async def list_user(self, user_id: UUID, size: int, page: int) -> list[Transaction]:
        return await self.t_repo.list_user(user_id, size, page)


    async def get_by_id(self, tx_id: int, user_id: UUID | None = None) -> Transaction | None:
        tx = await self.t_repo.get(tx_id)
        if tx is None:
            return None
        if user_id is not None and tx.user_id != user_id:
            return None
        
        return tx


    async def balance(self, user_id: UUID) -> Wallet:
        return await self.w_repo.get_for_user(user_id)
