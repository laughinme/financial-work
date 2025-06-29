from typing import Annotated
from fastapi import Depends, Request

from database.relational_db import (
    UoW,
    get_uow,
    IdentityInterface,
    UserInterface,
)
from .credentials_service import CredentialsService
from ..tokens import TokenService, get_token_service


async def get_credentials_service(
    request: Request,
    uow: Annotated[UoW, Depends(get_uow)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> CredentialsService:
    identity_repo = IdentityInterface(uow.session)
    user_repo = UserInterface(uow.session)

    return CredentialsService(
        request, identity_repo, user_repo, token_service, uow
    )
