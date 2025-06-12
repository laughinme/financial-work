from fastapi import HTTPException, status

class PortfolioNotFound(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail='Portfolio with this id not found')


class InsufficientFunds(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="It can be either insufficient funds or incorrect currency"
        )
