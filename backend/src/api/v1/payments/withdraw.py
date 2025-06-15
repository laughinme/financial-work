from typing import Annotated
from fastapi import Depends, HTTPException

from core.security import auth_user, AuthRouter
from domain.payments import CreatePayout
from service.payments import StripeService, get_stripe_service
from database.relational_db import User


router = AuthRouter()

@router.post(
    path="/withdraw",
    responses={
        412: {"description": "User must complete Stripe onboarding first"}
    }
)
async def request_withdrawal(
    payload: CreatePayout,
    service: Annotated[StripeService, Depends(get_stripe_service)],
    user: Annotated[User, Depends(auth_user)]
):
    if not user.stripe_onboarding_completed or not user.stripe_account_id:
        raise HTTPException(412, detail="User must complete Stripe onboarding first")
    
    await service.create_transfer(payload.amount, user.stripe_account_id)
    
    await service.create_payout_connect(payload.amount, user.stripe_account_id)
