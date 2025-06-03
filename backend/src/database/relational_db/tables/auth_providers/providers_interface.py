from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.users import Provider

from .providers_table import AuthProvider
from ..users import User


class AuthProvidersInterface:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add(
        self, 
        auth_provider: AuthProvider
    ) -> AuthProvider:
        self.session.add(auth_provider)
        return auth_provider


    async def find_for_provider(
        self,
        provider: Provider,
        identifier: str
    ) -> AuthProvider | None:
        result = await self.session.scalar(
            select(AuthProvider)
            .where(
                AuthProvider.provider_user_id == identifier,
                AuthProvider.provider == provider
            )
        )

        return result
