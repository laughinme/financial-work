import bcrypt

from fastapi import Request

from database.relational_db import UserInterface, User
from domain.users import UserRegister, UserLogin

from .exceptions import WrongCredentials, NotAuthenticated
from ..session import SessionService


class UserService():
    def __init__(
        self,
        user_repo: UserInterface,
        session_service: SessionService
    ):
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
    
    
    async def login(self, request: Request, payload: UserLogin) -> User:
        user = await self.user_repo.get_by_email(payload)
        if user is None:
            raise WrongCredentials()
        try:
            bcrypt.checkpw(payload.password.encode(), user.password.encode())
        except Exception as e:
            print(e)
            raise WrongCredentials()
        
        session_id = await self.session_service.create_session(user.id)
        request.session['session_id'] = session_id
        
        return user
    
    
    async def get_me(self, request: Request) -> User:
        session_id = request.session.get("session_id")
        if not session_id:
            raise NotAuthenticated()
        data = await self.session_service.get_session(session_id)
        if not data:
            raise NotAuthenticated()
        user_id = data['sub']
        
        user = await self.user_repo.get_user(user_id)
        return user
