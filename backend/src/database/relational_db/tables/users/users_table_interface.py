import random
import string

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users import UserRegister, UserLogin
from .users_table import User


class UserInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def create(self, payload: UserRegister) -> User:
        user = User(
            email=payload.email,
            phone_number=payload.phone_number,
            password=payload.password,
            secure_code="".join([random.choice(string.ascii_letters) for _ in range(64)]),
            secret=payload.secret
        )
        self.session.add(user)
        await self.session.commit()
        return user
        
        
    async def get_by_email(self, payload: UserLogin) -> User:
        query = (
            select(User)
            .where(
                User.email == str(payload.email),
                User.secret == payload.secret
            )
        )
        user = await self.session.scalar(query)
        return user
    
    
    async def get_user(self, user_id: str) -> User:
        user = await self.session.get(User, user_id)
        return user
