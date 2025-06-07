import json

from fastapi import APIRouter, Request, Depends

from service.payments import StripeService, get_stripe_service


router = APIRouter()

@router.post("/stripe", status_code=200)
async def receive_stripe_payment(
    request: Request,
    service: StripeService = Depends(get_stripe_service),
):
    body = json.loads(await request.body())
    await service.process_payment(body)
