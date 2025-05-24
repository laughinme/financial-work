from fastapi import HTTPException

class NotAuthenticated(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=401, detail='Not authenticated')
