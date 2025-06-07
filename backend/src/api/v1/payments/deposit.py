from fastapi import APIRouter, Depends

from core.security import auth_user
from domain.payments import CreatePaymentSchema, RedirectPaymentSchema
from service.payments import StripeService, get_stripe_service
from database.relational_db import User


router = APIRouter()

@router.post(
    path="/deposit",
    response_model=RedirectPaymentSchema,
    status_code=201
)
async def create_payment(
    payload: CreatePaymentSchema,
    service: StripeService = Depends(get_stripe_service),
    user: User = Depends(auth_user)
) -> RedirectPaymentSchema:
    url = await service.create_payment(payload, user)
    
    return RedirectPaymentSchema(url=url)
