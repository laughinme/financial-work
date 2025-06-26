from __future__ import annotations

import uuid
import math
import random
import asyncio
from enum import Enum
from datetime import date, timedelta, datetime, UTC
from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel, Field, field_validator


class DayRecord(BaseModel):
    date: date
    balance: Decimal
    equity: Decimal
    profit: Decimal
    floating_pl: Decimal
    pips: Decimal
    lots: Decimal
    deposit: Decimal = Decimal("0")
    withdrawal: Decimal = Decimal("0")


class Risk(Enum):
    """Level of strategy risk"""
    
    VERY_AGGRESSIVE = ((1.0, 1.4), (0.7, 1.2))
    AGGRESSIVE = ((0.5, 0.9), (0.3, 0.6))
    AVERAGE = ((0.2, 0.4), (0.15, 0.3))
    CONSERVATIVE = ((0.05, 0.25), (0.05, 0.12))


class PortfolioState(BaseModel):
    id: int
    balance: Decimal
    equity: Decimal
    deposits: Decimal
    withdrawals: Decimal
    floating_pl: Decimal = Decimal("0")
    history: dict[date, DayRecord] = Field(default_factory=dict)
    initial_equity: Decimal = Decimal("0")
    user_deposit: Decimal = Decimal("0")
    cash_cooldown: int = 0
    risk: Risk
    mu: float
    sigma: float
    last_update_date: datetime

    @field_validator("balance", "equity", "deposits", "withdrawals", "floating_pl", mode="before")
    @classmethod
    def _to_dec(cls, v):
        return Decimal(v)


STATE: dict[int, PortfolioState] = {}

