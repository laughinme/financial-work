import json

from fastapi import APIRouter, Request, Depends

from service.payments import YooKassaService, get_yookassa_service


router = APIRouter()

@router.post("/payment_succeded", status_code=200)
async def successful_payment(
    request: Request,
    service: YooKassaService = Depends(get_yookassa_service)
):
    body = json.loads(await request.body())
    await service.process_payment(body)
    
    
    