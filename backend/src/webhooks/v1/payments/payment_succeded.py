import json
import logging

from fastapi import APIRouter, Request, HTTPException
from yookassa.domain.notification import WebhookNotification


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/payment_succeded")
async def yookassa_webhook(request: Request):
    try:
        body = json.loads(await request.body())
        notification_object = WebhookNotification(body)
        event = notification_object.event
        object = notification_object.object

        if event == 'payment.succeeded':
            payment_id = object.id
            amount = object.amount.value
            currency = object.amount.currency
            logger.info(f"Платеж {payment_id} на сумму {amount} {currency} успешно завершен.")
        else:
            logger.warning(f"Получено уведомление о неподдерживаемом событии: {event}")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Ошибка при обработке уведомления: {str(e)}")
        raise HTTPException(status_code=400, detail="Ошибка при обработке уведомления")