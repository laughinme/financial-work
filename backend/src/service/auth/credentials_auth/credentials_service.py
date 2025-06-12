import bcrypt
import random 
import string

from fastapi import Request
from sqlalchemy.exc import IntegrityError

from database.relational_db import (
    UserInterface,
    User,
    CredentialsInterface,
    CredsProvider,
    AuthProvidersInterface,
    AuthProvider,
    UoW
)
from domain.users import Provider, UserRegister, UserLogin
from core.config import Config
from .exceptions import AlreadyExists, WrongCredentials
from ..session import SessionService


config = Config()


class CredentialsService:
    def __init__(
        self,
        creds_repo: CredentialsInterface,
        auth_repo: AuthProvidersInterface,
        user_repo: UserInterface,
        session_service: SessionService,
        uow: UoW
    ):
        self.creds_repo = creds_repo
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.session_service = session_service
        self.uow = uow
    
    
    async def register(
        self,
        request: Request,
        payload: UserRegister,
        ttl: int
    ) -> User:
        identifier = payload.email or payload.phone_number
        
        hashed_password = bcrypt.hashpw(
            password=payload.password.encode(),
            salt=bcrypt.gensalt()
        ).decode()
        
        user = User(
            secure_code="".join([random.choice(string.ascii_letters) for _ in range(64)]),
        )
        auth = AuthProvider(
            provider=Provider.CREDENTIALS,
            provider_user_id=identifier,
            credentials=CredsProvider(
                is_email=payload.email is not None,
                password=hashed_password
            )
        )
        user.providers.append(auth)
        await self.user_repo.add(user)
        
        try:
            await self.uow.session.flush()
        except IntegrityError:
            raise AlreadyExists()
        
        session_id = await self.session_service.create_session(user.id, ttl)
        request.session['session_id'] = session_id
        
        return user
    
    
    async def login(self, request: Request, payload: UserLogin, ttl: int) -> User:
        identifier = payload.email or payload.phone_number
        result = await self.creds_repo.get_user_and_password(identifier)
        if result is None:
            raise WrongCredentials()
        
        user, password = result
        try:
            is_valid = bcrypt.checkpw(payload.password.encode(), password.encode())
        except Exception:
            raise WrongCredentials()

        if not is_valid:
            raise WrongCredentials()
        
        session_id = await self.session_service.create_session(user.id, ttl)
        request.session['session_id'] = session_id
        
        return user
