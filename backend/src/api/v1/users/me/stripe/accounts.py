from typing import Annotated
from fastapi import Depends

from core.security import auth_user, AuthRouter
from database.relational_db import User
from domain.payments import StripeAccountLink
from service.payments import StripeService, get_stripe_service


router = AuthRouter()


@router.post(
    "/connect/onboarding-link",
    response_model=StripeAccountLink
)
async def get_onboarding_link(
    service: Annotated[StripeService, Depends(get_stripe_service)],
    user: Annotated[User, Depends(auth_user)]
):
    if not user.stripe_account_id:
        await service.connected_account(user)
        
    url = await service.create_account_link(
        user.stripe_account_id
    )
    
    return url
