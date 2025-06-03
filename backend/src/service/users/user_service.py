from fastapi import Request

from database.relational_db import UserInterface, User
from .exceptions import NotAuthenticated
from ..auth import SessionService


class UserService():
    def __init__(
        self,
        user_repo: UserInterface,
        session_service: SessionService
    ):
        self.user_repo = user_repo
        self.session_service = session_service
    
    
    async def get_me(self, request: Request) -> User:
        session_id = request.session.get("session_id")
        if not session_id:
            raise NotAuthenticated()
        data = await self.session_service.get_session(session_id)
        if not data:
            raise NotAuthenticated()
        user_id = data['sub']
        
        user = await self.user_repo.get_by_id(user_id)
        return user
