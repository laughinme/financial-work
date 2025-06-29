from fastapi import HTTPException

class InvalidTelegramSignature(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=401, detail='Invalid telegram signature')


class AlreadyLinked(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=409, detail='Telegram account already linked')
