import random
import string

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .users_table import User


class UserInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    
    @staticmethod
    def create() -> User:
        user = User(
            secure_code="".join([random.choice(string.ascii_letters) for _ in range(64)]),
        )
        return user
    
    
    async def add(self, user: User) -> User:
        self.session.add(user)
        return user
    
    
    async def get_by_id(self, id: UUID) -> User | None:
        user = await self.session.scalar(
            select(User)
            .where(
                User.id == id
            )
        )
        
        return user
