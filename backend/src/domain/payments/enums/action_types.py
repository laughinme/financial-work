from enum import Enum


class DepositAction(Enum):
    """
    For one-click payments you can choose an action and provide specific id
    """
    
    DEPOSIT = 'deposit'
    INVEST = 'invest'
