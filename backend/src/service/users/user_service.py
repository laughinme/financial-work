import jwt
from fastapi import Request

from domain.users import Role
from database.relational_db import UserInterface, User
from .exceptions import NotAuthenticated
from ..auth import TokenService


class UserService:
    def __init__(
        self,
        user_repo: UserInterface,
        token_service: TokenService
    ):
        self.user_repo = user_repo
        self.token_service = token_service
    
    
    async def get_me(self, request: Request) -> User | None:
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise NotAuthenticated()
        token = auth.split(" ", 1)[1]
        try:
            data = self.token_service.decode_access(token)
        except jwt.PyJWTError:
            raise NotAuthenticated()
        
        user_id = data['sub']
        user = await self.user_repo.get_by_id(user_id)

        return user
