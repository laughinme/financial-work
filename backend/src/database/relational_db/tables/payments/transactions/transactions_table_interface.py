from uuid import UUID
from datetime import date, timedelta
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from domain.payments import TransactionType
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
    
    
    async def cash_flow(self, user_id: UUID, days: int):
        start = date.today() - timedelta(days=days)

        day = func.date_trunc("day", Transaction.created_at)
        query = (
            select(
                day.label("date"),
                func.sum(
                    case((Transaction.type == TransactionType.DEPOSIT, Transaction.amount), else_=0)
                ).label("deposits"),
                func.sum(
                    case((Transaction.type == TransactionType.WITHDRAW, Transaction.amount), else_=0)
                ).label("withdrawals"),
            )
            .where(
                Transaction.user_id == user_id,
                Transaction.created_at >= start,
            )
            .group_by(day)
            .order_by(day)
        )
        result = await self.session.execute(query)
        
        return result.mappings().all()
