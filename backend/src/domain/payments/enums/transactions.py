from enum import Enum


class TransactionType(Enum):
    DEPOSIT          = "deposit"           # external deposit
    WITHDRAW_PENDING = 'withdraw_pending'  # freeze
    WITHDRAW         = "withdraw"          # external withdraw
    INVEST           = "invest"            # wallet → portfolio
    INVEST_PENDING   = "invest_pending"    # invest order
    PAYBACK          = "payback"           # portfolio → wallet (withdraw)
    PAYBACK_PENDING  = "payback_pending"   # payback order
    FEE              = "fee"               # success-fee
    PNL              = "pnl"               # revaluation +/-
