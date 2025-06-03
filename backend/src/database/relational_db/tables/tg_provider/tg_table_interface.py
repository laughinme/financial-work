from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users import Provider
from .telegram_user_table import TelegramProvider
from ..users import User
from ..auth_providers import AuthProvider


class TelegramInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    
    # async def add(
    #     self,
    #     telegram_provider: TelegramProvider
    # ) -> TelegramProvider:
    #     self.session.add(telegram_provider)
    #     return telegram_provider


    async def get_user_by_tg(
        self, identifier: str
    ) -> User | None:
        query = (
            select(User)
            .join(AuthProvider)
            .where(
                AuthProvider.provider == Provider.TELEGRAM,
                AuthProvider.provider_user_id == identifier,
            )
        )
        result = await self.session.scalar(query)
        return result
