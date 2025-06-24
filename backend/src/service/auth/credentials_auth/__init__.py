from typing import Annotated
from fastapi import Depends, Request

from database.relational_db import (
    UoW,
    get_uow,
    IdentityInterface,
    UserInterface,
)
from .credentials_service import CredentialsService
from ..session import get_session_service, SessionService


async def get_credentials_service(
    request: Request,
    uow: Annotated[UoW, Depends(get_uow)],
    session_service: Annotated[SessionService, Depends(get_session_service)],
) -> CredentialsService:
    identity_repo = IdentityInterface(uow.session)
    user_repo = UserInterface(uow.session)

    return CredentialsService(
        request, identity_repo, user_repo, session_service, uow
    )
