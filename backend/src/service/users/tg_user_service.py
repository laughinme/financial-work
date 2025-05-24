import bcrypt

from fastapi import Request

from database.relational_db import UserInterface, User
from domain.users import UserRegister, UserLogin

from .exceptions import WrongCredentials, NotAuthenticated
from ..session import SessionService


class TgAuthService():
    def __init__(
        self,
        tg_repo: UserInterface,
        user_repo: UserInterface,
        session_service: SessionService
    ):
        self.tg_repo = tg_repo
        self.user_repo = user_repo
        self.session_service = session_service
        
    
    async def register(self, request: Request, payload: UserRegister, ttl: int) -> User:
        hashed_password = bcrypt.hashpw(
            password=payload.password.encode(),
            salt=bcrypt.gensalt()
        )
        payload.password = hashed_password.decode()
        user = await self.user_repo.create(payload)
        
        session_id = await self.session_service.create_session(user.id, ttl)
        request.session['session_id'] = session_id
        
        return user
    
