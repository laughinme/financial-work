from fastapi import APIRouter, Depends

from core.security import auth_user
from domain.payments import CreatePayoutSchema
from service.payments import StripeService, get_stripe_service
from database.relational_db import User


router = APIRouter()

@router.post(
    path="/withdraw",
)
async def request_withdrawal(
    payload: CreatePayoutSchema,
    service: StripeService = Depends(get_stripe_service),
    user: User = Depends(auth_user)
):
    pass
