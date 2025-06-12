from enum import Enum


class PaymentProvider(Enum):
    YOOKASSA = 'yookassa'
    STRIPE = 'stripe'
    CRYPTO = 'crypto'
    YANDEX = 'yandex'
    TINKOFF = 'tinkoff'
    ROBOKASSA = 'robokassa'
    PAYANYWAY = 'payanyway'
