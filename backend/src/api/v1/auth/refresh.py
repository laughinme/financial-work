from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response, HTTPException

from service.auth import TokenService, get_token_service
from domain.users import AccessToken
from core.config import Config

router = APIRouter()
config = Config()


@router.post('/refresh', response_model=AccessToken)
async def refresh_tokens(
    request: Request,
    response: Response,
    token_service: Annotated[TokenService, Depends(get_token_service)]
) -> AccessToken:
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    tokens = await token_service.refresh_tokens(token)
    if tokens is None:
        response.delete_cookie("refresh_token")
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    access, refresh = tokens
    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=config.REFRESH_TTL,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return AccessToken(access_token=access)
