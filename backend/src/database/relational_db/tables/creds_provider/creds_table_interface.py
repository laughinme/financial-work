from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users import UserRegister, Provider
from .creds_table import CredsProvider
from ..auth_providers import AuthProvider
from ..users import User


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
    
    
    async def get_user_and_password(
        self, identifier: str
    ) -> tuple[User, str] | None:
        query = (
            select(User, CredsProvider.password)
            .join_from(User, AuthProvider)
            .join(CredsProvider)
            .where(
                AuthProvider.provider == Provider.CREDENTIALS,
                AuthProvider.provider_user_id == identifier,
            )
        )
        result = await self.session.execute(query)
        return result.one_or_none()
