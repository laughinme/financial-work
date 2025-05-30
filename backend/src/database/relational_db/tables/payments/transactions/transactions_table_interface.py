from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .transactions_table import Transaction


class TransactionInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def add(self, transaction: Transaction) -> None:
        self.session.add(transaction)
        
    
    
