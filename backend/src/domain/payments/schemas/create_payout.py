from pydantic import BaseModel
from decimal import Decimal


class CreatePayoutSchema(BaseModel):
    amount: Decimal # Необходимая сумма оплаты в формате double (100.00)
    description: str # Описание (Заказ №1, Пополнение {UUID} и т.д.)
