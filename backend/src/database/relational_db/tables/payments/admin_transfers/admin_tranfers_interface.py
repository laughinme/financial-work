from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .admin_transfers_table import AdminTransfer


class AdminTransferInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    
    async def add(self, intent: AdminTransfer) -> None:
        self.session.add(intent)
