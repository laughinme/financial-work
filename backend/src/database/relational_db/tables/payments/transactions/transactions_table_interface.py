from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .transactions_table import Transaction


class TransactionInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def add(self, transaction: Transaction) -> None:
        self.session.add(transaction)
        
    
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
