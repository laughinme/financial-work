from pydantic import BaseModel


class CreatePayoutSchema(BaseModel):
    value: str # Необходимая сумма оплаты в формате double (100.00)
    currency: str # Валюта (RUB, USD, EUR и т.д.)
    description: str # Описание (Заказ №1, Пополнение {UUID} и т.д.)
    card_number: str 
