from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .transactions_table import Transaction


class TransactionInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def add(self, transaction: Transaction) -> None:
        self.session.add(transaction)


    async def get(self, tx_id: int) -> Transaction | None:
        return await self.session.get(Transaction, tx_id)


    async def list_user(self, user_id: UUID, size: int, page: int) -> list[Transaction]:
        query = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self.session.scalars(query)
        
        return result.all()

    
    async def user_portfolio(
        self,
        user_id: UUID,
        portfolio_id: int
    ) -> list[Transaction]:
        query = (
            select(Transaction)
            .where(
                Transaction.user_id == user_id,
                Transaction.portfolio_id == portfolio_id
            )
        )
        result = await self.session.scalars(query)
        transactions = result.all()
        
        return transactions
