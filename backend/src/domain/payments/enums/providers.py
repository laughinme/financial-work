from enum import Enum


class PaymentProvider(Enum):
    YOOKASSA = 'yookassa'
    CRYPTO = 'crypto'
    YANDEX = 'yandex'
    TINKOFF = 'tinkoff'
    ROBOKASSA = 'robokassa'
    PAYANYWAY = 'payanyway'
