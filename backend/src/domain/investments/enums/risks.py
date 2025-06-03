from enum import Enum


class RiskScale(Enum):
    CONSERVATIVE = 'conservative'
    MOD_CONSERVATIVE = 'moderately_conservative'
    MOD_AGGRESSIVE = 'moderately_aggressive'
    AGGRESSIVE = 'aggressive'
    VERY_AGGRESSIVE = 'very_aggressive'
