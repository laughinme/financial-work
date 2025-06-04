from fastapi import APIRouter

from domain.payments.schemas import CreatePayoutSchema

from service.payments import YooKassaService


router = APIRouter()

@router.post(
    path="/withdraw",
)
async def request_withdrawal(payload: CreatePayoutSchema):
    return await YooKassaService.payout(payload)
