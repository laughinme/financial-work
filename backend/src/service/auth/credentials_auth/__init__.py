from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.relational_db import (
    get_db,
    CredentialsInterface,
    AuthProvidersInterface,
    UserInterface,
)
from .credentials_service import CredentialsService
from ..session import get_session_service, SessionService


async def get_credentials_service(
    session: AsyncSession = Depends(get_db),
    session_service: SessionService = Depends(get_session_service),
) -> CredentialsService:
    creds_repo = CredentialsInterface(session)
    auth_repo = AuthProvidersInterface(session)
    user_repo = UserInterface(session)
    
    return CredentialsService(
        creds_repo, auth_repo, user_repo, session_service
    )
