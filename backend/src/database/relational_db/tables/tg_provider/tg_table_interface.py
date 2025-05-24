from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from domain.users import TelegramAuth
from .telegram_user_table import TelegramUser


class TgUserInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    
    async def create(
        self,
        payload: TelegramAuth,
        user_id: UUID
    ) -> TelegramUser:
        user = TelegramUser(
            user_id=user_id,
            id=payload.id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            username=payload.username,
            photo_url=payload.photo_url,
        )
        self.session.add(user)
        await self.session.commit()
        
        
    async def get_by_tg_id(self, id: int) -> TelegramUser | None:
        user = await self.session.scalar(
            select(TelegramUser)
        )
        return user