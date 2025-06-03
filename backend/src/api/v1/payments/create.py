from fastapi import APIRouter

from domain.payments.schemas import CreatePaymentSchema, RedirectPaymentSchema

from service.payments import YooKassaService


router = APIRouter()

@router.post(
    path="/create",
    response_model=RedirectPaymentSchema
)
async def create_payment(payload: CreatePaymentSchema) -> RedirectPaymentSchema:
    url = await YooKassaService.create_payment(payload)
    return RedirectPaymentSchema(url=url)
