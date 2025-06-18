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

    @field_validator("balance", "equity", "deposits", "withdrawals", "floating_pl", mode="before")
    @classmethod
    def _to_dec(cls, v):
        return Decimal(v)

STATE: dict[int, PortfolioState] = {}


def quantize_(value: float | Decimal, cents: int = 2) -> Decimal:
    """Fast rounding to 2 digits."""
    step = Decimal("1").scaleb(-cents)
    return Decimal(value).quantize(step, ROUND_HALF_UP)


TRADING_DAYS_YEAR = 252
def gbm_daily(mu: float, sigma: float) -> float:
    """Profit r for 1 day on GBM."""
    dt = 1 / TRADING_DAYS_YEAR
    drift = (mu - 0.5 * sigma ** 2) * dt
    shock = sigma * math.sqrt(dt) * random.gauss(0, 1)
    
    return math.exp(drift + shock) - 1

def gen_profit(equity: Decimal, mu: float = .2, sigma: float = .25) -> Decimal:
    """P/L of the day, already rounded to the cent."""
    r = gbm_daily(mu, sigma)
    
    return quantize_(equity * Decimal(r))


def gen_floating_pl(equity: Decimal, sigma: float) -> Decimal:
    sigma_day  = sigma / math.sqrt(TRADING_DAYS_YEAR)
    sigma_intra = sigma_day * 0.4

    pct = random.gauss(0, sigma_intra)
    pct = max(min(pct,  3 * sigma_intra), -3 * sigma_intra)

    return quantize_(equity * Decimal(pct))


def maybe_cashflow(
    equity: Decimal,
    quiet_left: int,
    initial_equity: Decimal,
) -> tuple[Decimal, int]:
    if quiet_left > 0:
        return Decimal("0"), quiet_left - 1

    if random.random() >= 0.03:
        return Decimal("0"), 0

    sign = 1 if random.random() < 0.6 else -1

    frac  = quantize_(random.uniform(*(0.02, 0.08)))
    delta = quantize_(sign * frac * initial_equity)

    if abs(delta) < Decimal("50"):
        delta = Decimal("50") * sign
    if abs(delta) > Decimal("30000"):
        delta = Decimal("30000") * sign

    if sign == 1 and equity + delta > initial_equity * 5:
        delta = Decimal("0")
    elif sign == -1 and equity + delta < Decimal("0"):
        delta = -equity

    new_quiet = random.randint(*(3, 9))
    return delta, new_quiet


# History generation
DAY = timedelta(days=1)

def seed_history(
    p: PortfolioState,
    days_back: int = 365,
    user_deposit: Decimal | None = None,
):
    p.initial_equity = Decimal("10000")
    if user_deposit is None:
        user_deposit = quantize_(random.uniform(100, 10000))

    p.user_deposit = user_deposit
    equity = p.initial_equity + user_deposit
    balance = p.initial_equity + user_deposit
    deposits = p.initial_equity + user_deposit
    withdrawals = Decimal("0")
    quiet_left = 0

    start_day = date.today() - timedelta(days_back)

    for n in range(days_back):
        day = start_day + n * DAY

        deposit_today = Decimal("0")
        withdraw_today = Decimal("0")
        if n == 0:
            deposit_today = p.initial_equity + user_deposit

        # Deposit / Withdraw
        cash, quiet_left = maybe_cashflow(equity, quiet_left, p.initial_equity)
        if cash > 0:
            deposits += cash
            deposit_today += cash
        elif cash < 0:
            withdrawals -= cash
            withdraw_today += -cash
        balance += cash
        equity += cash

        # Trade result
        profit = gen_profit(equity, p.mu, p.sigma)
        balance += profit
        equity += profit

        # floatingPL ±1.2 % equity
        floating = gen_floating_pl(equity, p.sigma)
        if equity + floating < 0:
            floating = -equity

        rec = DayRecord(
            date = day,
            balance = balance,
            equity = equity + floating,
            profit = profit,
            floating_pl = floating,
            pips = quantize_(profit / Decimal("10")),
            lots = quantize_(abs(profit) / Decimal("1000")),
            deposit = deposit_today,
            withdrawal = withdraw_today,
        )
        p.history[day] = rec

    p.balance = balance
    p.equity = equity
    p.deposits = deposits
    p.withdrawals = withdrawals


def seed_portfolios(count: int = 10):
    if STATE:
        return
    
    for i in range(1, count + 1):
        risk = random.choice(list(Risk))
        p = PortfolioState(
            id=i,
            balance=Decimal("0"),
            equity=Decimal("0"),
            deposits=Decimal("0"),
            withdrawals=Decimal("0"),
            risk=risk,
            mu=random.uniform(*risk.value[0]),
            sigma=random.uniform(*risk.value[1])
        )
        seed_history(p, 365)
        STATE[i] = p


# Conversion to myfxbook format
def convert_state_to_account(p: PortfolioState) -> dict:
    total_profit = p.balance - p.deposits + p.withdrawals

    gain = Decimal("0")
    if p.deposits > 0:
        gain = quantize_(total_profit / p.deposits * 100, cents=3)

    peak = max((r.equity for r in p.history.values()), default=p.equity)
    drawdown = Decimal("0")
    if peak:
        drawdown = quantize_((peak - p.equity) / peak * 100, 3)

    equity_percent = quantize_(
        (p.equity / p.balance * 100) if p.balance else Decimal("0"), 3
    )

    first_day = min(p.history) if p.history else date.today()

    return {
        "id": p.id,
        "name": f"Portfolio {p.id}",
        "description": None,
        "accountId": p.id + 10_000,
        "gain": gain,
        "absGain": gain,
        "daily": Decimal("0"),
        "monthly": Decimal("0"),
        "withdrawals": p.withdrawals,
        "deposits": p.deposits,
        "interest": Decimal("0"),
        "profit": total_profit,
        "balance": p.balance,
        "drawdown": drawdown,
        "equity": p.equity,
        "equityPercent": equity_percent,
        "demo": True,
        "lastUpdateDate": datetime.now(UTC).strftime("%m/%d/%Y %H:%M"),
        "creationDate": first_day.strftime("%m/%d/%Y %H:%M"),
        "firstTradeDate": first_day.strftime("%m/%d/%Y %H:%M"),
        "tracking": 0,
        "views": 0,
        "commission": 0,
        "currency": "USD",
        "profitFactor": Decimal("1.50"),
        "pips": quantize_(sum(r.pips for r in p.history.values())),
        "portfolio": "Default",
        "invitationUrl": f"https://example.com/{uuid.uuid4()}",
        "server": {"name": "MockServer"},
        "risk": p.risk.name
    }


def convert_day_record(rec: DayRecord) -> list[dict]:
    return [
        {
            "date": rec.date.strftime("%m/%d/%Y"),
            "balance": rec.balance,
            "pips": rec.pips,
            "lots": rec.lots,
            "floatingPL": rec.floating_pl,
            "profit": rec.profit,
            "growthEquity": rec.equity,
            "floatingPips": quantize_(rec.floating_pl / Decimal("10")),
            "deposit": rec.deposit,
            "withdrawal": rec.withdrawal,
        }
    ]


def convert_day_gain(
    rec: DayRecord,
    prev_eq: Decimal,
) -> dict:
    """Gain % for a particular day."""
    gain = Decimal("0") if prev_eq == 0 else quantize_((rec.equity/prev_eq-1)*100, 3)
    return [{
        "date":   rec.date.strftime("%m/%d/%Y"),
        "value":  gain,
        "profit": rec.profit,
    }]


def upsert_today_record(
    p: PortfolioState,
    deposit_delta: Decimal = Decimal("0"),
    withdraw_delta: Decimal = Decimal("0"),
    profit_delta: Decimal = Decimal("0"),
) -> None:
    today = date.today()
    record = p.history.get(today)
    if not record:
        record = DayRecord(
            date=today,
            balance=p.balance,
            equity=p.equity,
            profit=profit_delta,
            floating_pl=p.floating_pl,
            pips=Decimal("0"),
            lots=Decimal("0.1"),
            deposit=deposit_delta,
            withdrawal=withdraw_delta,
        )
    else:
        record.balance = p.balance
        record.equity = p.equity
        record.profit += profit_delta
        record.floating_pl = p.floating_pl
        record.deposit += deposit_delta
        record.withdrawal += withdraw_delta
    p.history[today] = record


async def simulate_realtime(period: float = 5 * 60) -> None:
    """Continuously mutate portfolio state to mimic trading."""
    
    while True:
        for p in STATE.values():
            cash, p.cash_cooldown = maybe_cashflow(p.equity, p.cash_cooldown, p.initial_equity)
            
            if cash > 0:
                p.deposits += cash
                dep = cash
                wd = Decimal("0")
            elif cash < 0:
                p.withdrawals -= cash
                dep = Decimal("0")
                wd = -cash
            else:
                dep = wd = Decimal("0")
                
            p.balance += cash
            p.equity += cash

            profit = gen_profit(p.equity, p.mu, p.sigma)
            p.balance += profit
            p.equity += profit

            p.floating_pl = gen_floating_pl(p.equity, p.sigma)
            upsert_today_record(p, dep, wd, profit)

        await asyncio.sleep(period)
