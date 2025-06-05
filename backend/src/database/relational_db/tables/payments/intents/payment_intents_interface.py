from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .payment_intents_table import PaymentIntent


class PaymentIntentInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def add(self, intent: PaymentIntent) -> None:
        self.session.add(intent)
