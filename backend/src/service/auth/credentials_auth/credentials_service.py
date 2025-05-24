import bcrypt

from fastapi import Request

from database.relational_db import UserInterface, User, CredentialsInterface, AuthProvidersInterface
from domain.users import Provider, UserRegister, UserLogin
from core.config import Config
from .exceptions import AlreadyExists, WrongCredentials
from ..session import SessionService


config = Config()


class CredentialsService():
    def __init__(
        self,
        creds_repo: CredentialsInterface,
        auth_repo: AuthProvidersInterface,
        user_repo: UserInterface,
        session_service: SessionService
    ):
        self.creds_repo = creds_repo
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.session_service = session_service
    
    
    async def register(
        self,
        request: Request,
        payload: UserRegister,
        ttl: int
    ) -> User:
        # TODO: Add transaction atomicity and remove find request
        
        provider_user_id = payload.email or payload.phone_number
        
        provider = await self.auth_repo.find_for_provider(Provider.CREDENTIALS, provider_user_id)
        if provider:
            raise AlreadyExists()
        
        user = await self.user_repo.create()
        provider = await self.auth_repo.create(Provider.CREDENTIALS, provider_user_id, user)
        
        hashed_password = bcrypt.hashpw(
            password=payload.password.encode(),
            salt=bcrypt.gensalt()
        )
        payload.password = hashed_password.decode()
        
        await self.creds_repo.create(provider.id, payload)
        
        session_id = await self.session_service.create_session(user.id, ttl)
        request.session['session_id'] = session_id
        
        return user
    
    
    async def login(self, request: Request, payload: UserLogin, ttl: int) -> User:
        provider_user_id = payload.email or payload.phone_number
        provider = await self.auth_repo.find_for_provider(Provider.CREDENTIALS, provider_user_id)
        if provider is None:
            raise WrongCredentials()
        
        credentials_provider = await self.creds_repo.get_by_id(provider.id)
        
        try:
            bcrypt.checkpw(payload.password.encode(), credentials_provider.password.encode())
        except Exception as e:
            print(e)
            raise WrongCredentials()
        
        user = await self.user_repo.get_user(provider.user_id)
        
        session_id = await self.session_service.create_session(user.id, ttl)
        request.session['session_id'] = session_id
        
        return user
