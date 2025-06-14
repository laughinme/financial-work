import bcrypt
import random 
import string
from uuid import UUID
from datetime import datetime, UTC

from fastapi import Request
from sqlalchemy.exc import IntegrityError

from database.relational_db import (
    UserInterface,
    User,
    IdentityInterface,
    Identity,
    UoW,
)
from domain.users import Provider, UserRegister, UserLogin
from core.config import Config
from .exceptions import AlreadyExists, WrongCredentials, NotAuthenticated
from ..session import SessionService


config = Config()


class CredentialsService:
    def __init__(
        self,
        request: Request,
        identity_repo: IdentityInterface,
        user_repo: UserInterface,
        session_service: SessionService,
        uow: UoW,
    ):
        self.identity_repo = identity_repo
        self.user_repo = user_repo
        self.session_service = session_service
        self.uow = uow
        self.request = request
    
    
    async def register(
        self,
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
            allow_password_login=True,
        )
        identity = Identity(
            provider=Provider.PASSWORD,
            external_id=identifier,
            secret_hash=hashed_password,
            verified=False,
            meta={"is_email": payload.email is not None},
            # last_login_at=datetime.now(UTC)
        )
        user.identities.append(identity)
        await self.user_repo.add(user)
        
        try:
            await self.uow.session.flush()
        except IntegrityError as e:
            raise AlreadyExists()
        
        session_id = await self.session_service.create_session(user.id, ttl)
        self.request.session['session_id'] = session_id
        
        return user
    
    
    async def login(self, payload: UserLogin, ttl: int) -> User:
        identifier = payload.email or payload.phone_number
        result = await self.identity_repo.get_user_and_secret(identifier)
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
        self.request.session['session_id'] = session_id
        
        return user
    
    
    async def logout(self) -> None:
        session_id = self.request.session['session_id']
        
        await self.session_service.revoke_session(session_id)


    async def link(self, identifier: str, user: User) -> None:
        """Link additional email or phone to the user."""
        base_identity = await self.identity_repo.find_password_by_user_id(user.id)
        if base_identity is None:
            raise NotAuthenticated

        existing = await self.identity_repo.find(Provider.PASSWORD, identifier)
        if existing is not None:
            raise AlreadyExists()

        identity = Identity(
            user_id=user.id,
            provider=Provider.PASSWORD,
            external_id=identifier,
            secret_hash=base_identity.secret_hash,
            verified=False,
            meta={"is_email": "@" in identifier},
        )

        await self.identity_repo.add(identity)

        try:
            await self.uow.session.flush()
        except IntegrityError:
            raise AlreadyExists()
