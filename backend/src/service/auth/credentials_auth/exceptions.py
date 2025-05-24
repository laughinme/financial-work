from fastapi import HTTPException, status

class WrongCredentials(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong credentials passed')

class NotAuthenticated(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')

class AlreadyExists(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='This email or phone number is already taken'
        )
