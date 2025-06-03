from enum import Enum


class TransactionType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    FEE = 'fee'
    PNL = 'pnl'
    PAYBACK = 'payback'
