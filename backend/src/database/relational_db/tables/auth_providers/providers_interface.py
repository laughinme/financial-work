from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.users import Provider

from .providers_table import AuthProvider
from ..users import User


class AuthProvidersInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def create(
        self, 
        provider: Provider,
        provider_user_id: str,
        user: User
    ) -> AuthProvider:
        new_provider = AuthProvider(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id
        )
        self.session.add(new_provider)
        await self.session.commit()
        
        return new_provider
    
    
    async def find_for_provider(
        self,
        provider: Provider,
        provider_user_id: str
    ) -> AuthProvider | None:
        result = await self.session.scalar(
            select(AuthProvider)
            .where(
                AuthProvider.provider_user_id == provider_user_id,
                AuthProvider.provider == provider
            )
        )
        
        return result
    
    
    