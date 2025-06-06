from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.payments import PaymentStatus
from .payment_intents_table import PaymentIntent


class PaymentIntentInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    
    async def add(self, intent: PaymentIntent) -> None:
        self.session.add(intent)
        
        
    async def get(self, intent_id: UUID) -> PaymentIntent:
        return await self.session.get(PaymentIntent, intent_id)


    async def update_status(self, intent_id: UUID, status: PaymentStatus) -> None:
        await self.session.execute(
            update(PaymentIntent)
            .values(status=status)
            .where(PaymentIntent.id == intent_id)
        )
        
    