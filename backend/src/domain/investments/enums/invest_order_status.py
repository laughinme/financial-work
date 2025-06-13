from enum import Enum


class InvestOrderStatus(Enum):
    """
    Represents status of investment in order.
    When placed, status 'pending' is given.
    When admin takes funds to place on investment account, status 'accepted' is given
    When cron job confirms funds transfer, status 'executed' is given.
    """
    
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    EXECUTED = 'executed'
    FAILED = 'failed'
