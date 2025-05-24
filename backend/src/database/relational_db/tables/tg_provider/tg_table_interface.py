from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users import TelegramAuthSchema
from .telegram_user_table import TelegramProvider


class TelegramInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    
    async def create(
        self,
        payload: TelegramAuthSchema,
        auth_providers_id: int
    ) -> TelegramProvider:
        user = TelegramProvider(
            id=auth_providers_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            username=payload.username,
            photo_url=payload.photo_url,
        )
        self.session.add(user)
        await self.session.commit()
        
        
    async def get_by_id(self, auth_providers_id: int) -> TelegramProvider | None:
        user = await self.session.scalar(
            select(TelegramProvider)
            .where(TelegramProvider.id == auth_providers_id)
        )
        
        return user
