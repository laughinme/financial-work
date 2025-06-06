from fastapi import HTTPException, status

class PaymentFailed(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail='Payment failed')

class UnsupportedEvent(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='YooKassa responded with unsupported event type'
        )

