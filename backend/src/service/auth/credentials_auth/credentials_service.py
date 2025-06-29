import random
import string

from uuid import UUID
from fastapi import Request
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from database.relational_db import (
    UserInterface,
    User,
    IdentityInterface,
    UoW,
    Wallet
)
from domain.users import Provider, UserRegister, UserLogin
from core.config import Config
from .exceptions import AlreadyExists, WrongCredentials, NotAuthenticated, NotFound, EmailAlreadySet
from ..tokens import TokenService


config = Config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CredentialsService:
    def __init__(
        self,
        request: Request,
        identity_repo: IdentityInterface,
        user_repo: UserInterface,
        token_service: TokenService,
        uow: UoW,
    ):
        self.identity_repo = identity_repo
        self.user_repo = user_repo
        self.token_service = token_service
        self.uow = uow
        self.request = request
        
        
    @staticmethod
    def _check_password(password: str, password_hash: bytes) -> bool:
        try:
            valid = pwd_context.verify(password.encode(), password_hash)
            if not valid:
                raise WrongCredentials()
        except ValueError:
            raise WrongCredentials()
        
        return valid
        
    @staticmethod
    def _hash_password(password: str) -> bytes:
        return pwd_context.hash(password).encode()
        
    
    async def register(
        self,
        payload: UserRegister
    ) -> User:
        
        password_hash = self._hash_password(payload.password)

        user = User(
            secure_code="".join([random.choice(string.ascii_letters) for _ in range(64)]),
            email=payload.email,
            password_hash=password_hash,
            allow_password_login=True,
        )
        
        wallet = Wallet(currency='USD')
        user.wallets.append(wallet)
        
        await self.user_repo.add(user)
        
        try:
            await self.uow.session.flush()
        except IntegrityError as e:
            raise AlreadyExists()
        
        access, refresh = await self.token_service.create_tokens(user.id)
        return access, refresh
    
    
    async def login(self, payload: UserLogin) -> User:
        user = await self.user_repo.get_by_email(payload.email)
        if user is None:
            raise WrongCredentials()

        self._check_password(payload.password, user.password_hash)
        
        access, refresh = await self.token_service.create_tokens(user.id)
        return access, refresh
    
    
    async def logout(self, refresh_token: str) -> None:
        await self.token_service.revoke(refresh_token)


    async def link(self, user_id: UUID, payload: UserRegister) -> None:
        """Completing profile"""
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFound()
        
        if user.email is not None:
            raise EmailAlreadySet()
        
        password_hash = self._hash_password(payload.password)

        user.email = payload.email
        user.password_hash = password_hash
