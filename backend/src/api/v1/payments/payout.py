from fastapi import APIRouter

from domain.payments.schemas import CreatePayoutSchema

from service.payments import YooKassaService


router = APIRouter()

@router.post(
    path="/payout",
)
async def payout_route(payload: CreatePayoutSchema):
    return await YooKassaService.payout(payload)
    