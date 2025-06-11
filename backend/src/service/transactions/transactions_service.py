from uuid import UUID

from database.relational_db import UoW, TransactionInterface, Transaction


class TransactionsService:
    def __init__(self, uow: UoW, repo: TransactionInterface):
        self.uow = uow
        self.repo = repo

    async def list_user(self, user_id: UUID, size: int, page: int) -> list[Transaction]:
        return await self.repo.list_user(user_id, size, page)

    async def get_by_id(self, tx_id: int, user_id: UUID | None = None) -> Transaction | None:
        tx = await self.repo.get(tx_id)
        if tx is None:
            return None
        if user_id is not None and tx.user_id != user_id:
            return None
        return tx

    async def list_for_user(self, user_id: UUID, size: int, page: int) -> list[Transaction]:
        return await self.repo.list_user(user_id, size, page)
