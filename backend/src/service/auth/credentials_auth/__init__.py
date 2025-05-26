from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    CredentialsInterface,
    AuthProvidersInterface,
    UserInterface,
)
from .credentials_service import CredentialsService
from ..session import get_session_service, SessionService


async def get_credentials_service(
    uow: UoW = Depends(get_uow),
    session_service: SessionService = Depends(get_session_service),
) -> CredentialsService:
    creds_repo = CredentialsInterface(uow.session)
    auth_repo = AuthProvidersInterface(uow.session)
    user_repo = UserInterface(uow.session)
    
    return CredentialsService(
        creds_repo, auth_repo, user_repo, session_service, uow
    )
