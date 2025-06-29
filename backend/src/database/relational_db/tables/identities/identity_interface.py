from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users import Provider
from .identity_table import Identity
from ..users import User


class IdentityInterface:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, identity: Identity) -> Identity:
        self.session.add(identity)
        return identity

    async def find(self, provider: Provider, identifier: str) -> Identity | None:
        return await self.session.scalar(
            select(Identity).where(
                Identity.provider == provider,
                Identity.external_id == identifier,
            )
        )
        
    async def get_user_by_provider(self, provider: Provider, identifier: str) -> User | None:
        query = (
            select(User)
            .join(Identity)
            .where(
                Identity.provider == provider,
                Identity.external_id == identifier,
            )
        )
        return await self.session.scalar(query)
