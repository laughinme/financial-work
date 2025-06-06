from enum import Enum


class InvestOrderStatus(Enum):
    PENDING = 'pending'
    EXECUTED = 'executed'
    FAILED = 'failed'
