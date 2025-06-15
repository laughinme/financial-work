from typing import Annotated
from fastapi import Depends

from core.security import auth_user, AuthRouter
from domain.payments import CreatePayment, RedirectPaymentSchema
from service.payments import StripeService, get_stripe_service
from database.relational_db import User


router = AuthRouter()

@router.post(
    path="/deposit",
    response_model=RedirectPaymentSchema,
    status_code=201
)
async def create_payment(
    payload: CreatePayment,
    service: Annotated[StripeService, Depends(get_stripe_service)],
    user: Annotated[User, Depends(auth_user)]
) -> RedirectPaymentSchema:
    url = await service.create_payment(payload, user)
    return url
