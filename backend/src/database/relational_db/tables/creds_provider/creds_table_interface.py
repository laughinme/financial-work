from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users import UserRegister
from .creds_table import CredsProvider


class CredentialsInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def create(
        self,
        auth_providers_id: int,
        payload: UserRegister
    ) -> CredsProvider:
        
        creds = CredsProvider(
            id=auth_providers_id,
            is_email=payload.phone_number is None,
            password=payload.password
        )
        self.session.add(creds)
        await self.session.commit()
        
        return creds
        
        
    async def get_by_id(
        self,
        auth_providers_id: int
    ) -> CredsProvider:
        provider = await self.session.scalar(
            select(CredsProvider)
            .where(CredsProvider.id == auth_providers_id)
        )
        
        return provider
