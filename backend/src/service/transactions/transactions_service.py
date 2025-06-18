from uuid import UUID

from database.relational_db import (
    UoW, TransactionInterface, Transaction, WalletInterface, Wallet
)


class TransactionsService:
    def __init__(
        self,
        uow: UoW,
        tx_repo: TransactionInterface,
        w_repo: WalletInterface
        
    ):
        self.uow = uow
        self.tx_repo = tx_repo
        self.w_repo = w_repo


    async def list_user(self, user_id: UUID, size: int, page: int) -> list[Transaction]:
        return await self.tx_repo.list_user(user_id, size, page)


    async def get_by_id(self, tx_id: int, user_id: UUID | None = None) -> Transaction | None:
        tx = await self.tx_repo.get(tx_id)
        if tx is None:
            return None
        if user_id is not None and tx.user_id != user_id:
            return None
        
        return tx


    async def balance(self, user_id: UUID) -> Wallet | None:
        return await self.w_repo.get_for_user(user_id)

    
    async def cashflow(self, user_id: UUID, days: int) -> list:
        return await self.tx_repo.cash_flow(user_id, days)
