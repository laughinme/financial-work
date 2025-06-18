from decimal import Decimal
from uuid import UUID
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from .wallets_table import Wallet


class WalletInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def add(self, obj: Wallet) -> None:
        await self.session.add(obj)
        
        
    async def get_for_user(self, user_id: UUID) -> Wallet | None:
        return await self.session.scalar(
            select(Wallet)
            .where(
                Wallet.user_id == user_id,
                Wallet.currency == 'USD'
            )
        )
        
    
    async def credit(
        self,
        user_id: UUID,
        currency: str,
        amount: Decimal
    ) -> Wallet:
        """
        Credit: add amount > 0
        """
        if amount < 0:
            raise ValueError('Amount cant be less than zero')
        
        query = (
            insert(Wallet)
            .values(
                user_id = user_id,
                currency = currency,
                balance = amount,
                locked = Decimal("0"),
            )
            .on_conflict_do_update(
                constraint='pk_wallets',
                set_={
                    "balance": Wallet.balance + amount
                }
            )
            .returning(Wallet)
        )
        result = await self.session.execute(query)
        
        return result.scalar()
        
        
    async def debit(
        self,
        user_id: UUID,
        currency: str,
        amount: Decimal
    ) -> Wallet | None:
        """
        Debit: subtract amount > 0
        """
        if amount < 0:
            raise ValueError('Amount cant be less than zero')
        
        query = (
            update(Wallet)
            .values(
                balance = Wallet.balance - amount
            )
            .where(
                Wallet.user_id == user_id,
                Wallet.currency == currency,
                Wallet.balance >= amount
            )
            .returning(Wallet)
        )
        result = await self.session.execute(query)
        
        return result.scalar()
    
    
    async def freeze(
        self,
        user_id: UUID,
        currency: str,
        amount: Decimal
    ) -> Wallet | None:
        """
        Balance - amount; locked + amount
        """
        query = (
            update(Wallet)
            .where(
                Wallet.user_id == user_id,
                Wallet.currency == currency,
                Wallet.balance >= amount
            )
            .values(
                balance = Wallet.balance - amount,
                locked = Wallet.locked + amount
            )
            .returning(Wallet)
        )
        result = await self.session.execute(query)
        
        return result.scalar()
    
    
    async def withdraw(
        self,
        user_id: UUID,
        currency: str,
        amount: Decimal
    ):
        """
        Complete withdrawal
        """
        query = (
            update(Wallet)
            .where(
                Wallet.user_id == user_id,
                Wallet.currency == currency,
                Wallet.locked >= amount
            )
            .values(
                locked = Wallet.locked - amount
            )
            .returning(Wallet)
        )
        
        result = await self.session.execute(query)
        
        return result.scalar()
    
    
    # TODO: handle transfer and payouts properly
    async def cancel_withdrawal(
        self,
        user_id: UUID,
        currency: str,
        amount: Decimal
    ):
        """
        Cancel withdrawal
        """
        query = (
            update(Wallet)
            .where(
                Wallet.user_id == user_id,
                Wallet.currency == currency,
                Wallet.locked >= amount
            )
            .values(
                locked = Wallet.locked - amount,
                balance = Wallet.balance + amount
            )
            .returning(Wallet)
        )
        
        result = await self.session.execute(query)
        
        return result.scalar()
