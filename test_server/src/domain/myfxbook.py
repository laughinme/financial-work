from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
import random

from pydantic import BaseModel, Field


class DayRecord(BaseModel):
    date: date
    balance: Decimal
    equity: Decimal
    profit: Decimal
    floating_pl: Decimal = Field(..., alias='floatingPL')
    pips: Decimal
    lots: Decimal


class PortfolioState(BaseModel):
    id: int
    balance: Decimal
    equity: Decimal
    deposits: Decimal
    withdrawals: Decimal
    floating_pl: Decimal = Decimal('0')
    history: dict[date, DayRecord] = {}
    initial_equity: Decimal = Decimal('0')


STATE: dict[int, PortfolioState] = {}


def seed_history(p: PortfolioState, days_back: int = 365 * 2) -> None:
    equity = Decimal('100000')
    p.balance = equity
    p.equity = equity
    p.deposits = equity
    p.withdrawals = Decimal('0')
    p.initial_equity = equity
    start_date = date.today() - timedelta(days=days_back)
    for n in range(days_back):
        day = start_date + timedelta(days=n)
        profit = (Decimal(random.uniform(-0.002, 0.002)) * equity).quantize(Decimal('0.01'))
        equity += profit
        record = DayRecord(
            date=day,
            balance=equity,
            equity=equity,
            profit=profit,
            floatingPL=Decimal('0'),
            pips=(profit / Decimal('10')).quantize(Decimal('0.01')),
            lots=Decimal('0.1')
        )
        p.history[day] = record
    p.balance = equity
    p.equity = equity


def convert_state_to_account(p: PortfolioState) -> dict:
    gain = ((p.equity / p.initial_equity) - 1) * Decimal('100')
    peak = max((r.equity for r in p.history.values()), default=p.equity)
    drawdown = ((peak - p.equity) / peak * Decimal('100')) if peak else Decimal('0')
    total_profit = p.balance - p.deposits + p.withdrawals
    return {
        'id': p.id,
        'name': f'Portfolio {p.id}',
        'description': None,
        'accountId': p.id + 1000,
        'gain': round(gain, 3),
        'absGain': round(gain, 3),
        'daily': 0,
        'monthly': 0,
        'withdrawals': int(p.withdrawals),
        'deposits': p.deposits,
        'interest': 0,
        'profit': total_profit,
        'balance': p.balance,
        'drawdown': round(drawdown, 3),
        'equity': p.equity,
        'equityPercent': round((p.equity / p.balance * Decimal('100')) if p.balance else Decimal('0'), 3),
        'demo': False,
        'lastUpdateDate': date.today().strftime('%m/%d/%Y %H:%M'),
        'creationDate': list(p.history.keys())[1].strftime('%m/%d/%Y %H:%M'),
        'firstTradeDate': list(p.history.keys())[1].strftime('%m/%d/%Y %H:%M'),
        'tracking': 0,
        'views': 0,
        'commission': 0,
        'currency': 'USD',
        'profitFactor': 1.5,
        'pips': sum(r.pips for r in p.history.values()),
        'portfolio': 'Default',
        'invitationUrl': 'http://example.com',
        'server': {'name': 'MockServer'}
    }


def convert_day_record(r: DayRecord) -> dict:
    return [{
        'date': r.date.strftime('%m/%d/%Y'),
        'balance': r.balance,
        'pips': r.pips,
        'lots': r.lots,
        'floatingPL': r.floating_pl,
        'profit': r.profit,
        'growthEquity': r.equity,
        'floatingPips': r.floating_pl / Decimal('10')
    }]


def convert_day_gain(r: DayRecord, initial_equity: Decimal) -> dict:
    gain = ((r.equity / initial_equity) - 1) * Decimal('100')
    return [{
        'date': r.date.strftime('%m/%d/%Y'),
        'value': gain,
        'profit': r.profit
    }]


def upsert_today_record(p: PortfolioState) -> None:
    today = date.today()
    record = p.history.get(today)
    if not record:
        record = DayRecord(
            date=today,
            balance=p.balance,
            equity=p.equity,
            profit=Decimal('0'),
            floatingPL=p.floating_pl,
            pips=Decimal('0'),
            lots=Decimal('0.1')
        )
    else:
        record.balance = p.balance
        record.equity = p.equity
    p.history[today] = record
