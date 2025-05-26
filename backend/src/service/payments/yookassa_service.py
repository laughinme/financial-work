import asyncio

import uuid_utils
import yookassa

from core.config import Config

config = Config()

yookassa.Configuration.account_id = config.YOOKASSA_ACCOUNT_ID
yookassa.Configuration.secret_key = config.YOOKASSA_SECRET


class YooKassaService:
    @staticmethod 
    async def create_payment(payload):
        return await asyncio.to_thread(YooKassaService._create_payment, payload)
    
    @staticmethod
    def _create_payment(payload):
        return yookassa.Payment.create(
        {
            "amount": {
                "value": payload.value,
                "currency": payload.currency
            },
            "confirmation": {
                "type": "redirect",
                "return_url": config.SITE_URL
            },
            "description": payload.description
        }, uuid_utils.uuid7()
        )["confirmation"]["confirmation_url"]
    
    @staticmethod
    async def get_payment_info(uuid: str) -> dict:
        return await asyncio.to_thread(YooKassaService._get_payment_info, uuid)

    @staticmethod
    def _get_payment_info(uuid: str) -> dict:
        return yookassa.Payment.find_one(uuid)