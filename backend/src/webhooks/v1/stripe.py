import json

from fastapi import APIRouter, Request, Depends, HTTPException

from service.payments import StripeService, get_stripe_service


router = APIRouter()

@router.post("/stripe", status_code=200)
async def stripe_webhook(
    request: Request,
    service: StripeService = Depends(get_stripe_service),
):
    try:
        body = json.loads(await request.body())
    except json.decoder.JSONDecodeError as e:
        raise HTTPException(502, detail='Webhook error while parsing basic request: ' + str(e))
    
    await service.process_webhook(body)
