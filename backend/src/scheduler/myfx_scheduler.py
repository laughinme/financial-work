import httpx
import logging
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from database.relational_db import get_uow_manually, PortfolioInterface, GainsInterface, HoldingsInterface
from database.redis import get_redis, CacheRepo
from service.myfxbook import MyFXService
from service.investments import InvestmentService, get_investment_service
from domain.myfxbook import DayData
from domain.users import DUMMY_USER_ID


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_drawdown(hist: list[DayData], current_eq: Decimal) -> Decimal:
    for index, day in enumerate(hist):
        if day.date == date.today():
            break
    peak = max((d.balance + d.floating_PL) for d in hist[:index+1]) if hist else current_eq
    if peak == 0:
        return Decimal('0')
    return ((peak - current_eq) / peak * 100).quantize(Decimal('0.001'), ROUND_HALF_UP)


async def myfx_job():
    async with get_uow_manually() as uow, httpx.AsyncClient(timeout=15) as client:
        cache_repo = CacheRepo(get_redis())
        service = MyFXService(uow, cache_repo, client)
        invest_service: InvestmentService = await get_investment_service(uow)
        p_repo = PortfolioInterface(uow.session)
        g_repo = GainsInterface(uow.session)
        h_repo = HoldingsInterface(uow.session)
        
        # Parsing data and updating database
        today = date.today()
        
        portfolios = await p_repo.list_all()
        by_oid = {p.oid_myfx: p for p in portfolios}
        
        result = (await service.get_accounts()).accounts
        accounts = {account.id: account for account in result}
        
        update_rows, snapshot_rows, gain_rows = [], [], []
        
        new_oids = set(accounts) - set(by_oid)
        if new_oids:
            portfolios_to_add = await p_repo.bulk_insert_from_accounts([accounts[oid] for oid in new_oids])
            for p in portfolios_to_add:
                daily_history = (await service.get_data_daily(p.oid_myfx, p.first_trade_at.date(), today)).data_daily
                daily_gain = (await service.get_daily_gain(p.oid_myfx, p.first_trade_at.date(), today)).daily_gain

                units_total = Decimal("0")
                nav = Decimal("1")
                for idx, day in enumerate(daily_history):
                    if idx == 0:
                        units_total = day.growth_equity
                        nav = Decimal("1")
                        drawdown = calculate_drawdown(daily_history, day.growth_equity)
                        snapshot_rows.append(
                            p_repo._snapshot_row(p.id, day.date, nav, day.balance, day.growth_equity, drawdown)
                        )
                        continue

                    if day.deposit:
                        units = (day.deposit / nav).quantize(Decimal("0.00000001"))
                        units_total += units
                        await h_repo.issue_units(DUMMY_USER_ID, p.id, units, day.deposit, nav)
                        holding = await h_repo.user_portfolio_holding(DUMMY_USER_ID, p.id)
                        await h_repo.insert_snapshot(holding)

                    if day.withdrawal:
                        units = (day.withdrawal / nav).quantize(Decimal("0.00000001"))
                        if await h_repo.burn_units(DUMMY_USER_ID, p.id, units, day.withdrawal):
                            units_total -= units
                            holding = await h_repo.user_portfolio_holding(DUMMY_USER_ID, p.id)
                            await h_repo.insert_snapshot(holding)
                            
                    await h_repo.revalue_holdings()

                    nav = invest_service.calc_nav_price(day.growth_equity, units_total)
                    drawdown = calculate_drawdown(daily_history[:idx+1], day.growth_equity)
                    snapshot_rows.append(
                        p_repo._snapshot_row(p.id, day.date, nav, day.balance, day.growth_equity, drawdown)
                    )

                gain_rows.extend(g_repo._gain_row(p.id, gain) for gain in daily_gain)
                update_rows.append(p_repo._portfolio_row(p.id, accounts[p.oid_myfx], nav, units_total))
                
            
        start = today - timedelta(days=365*2)
        daily_data = await service.bulk_data_daily(*accounts.keys(), start=start, end=today)
        daily_gain = await service.bulk_daily_gain(*accounts.keys(), start=start, end=today)
        deposit_p_ids = set()

        for p in portfolios:
            acc = accounts.get(p.oid_myfx)
            hist = daily_data.get(p.oid_myfx).data_daily
            gain = daily_gain.get(p.oid_myfx).daily_gain
            
            if p.last_update_myfx < acc.last_update_date:
                if p.deposits != acc.deposits or p.withdrawals != acc.withdrawals:
                    delta_deposit = acc.deposits - p.deposits
                    delta_withdrawal = acc.withdrawals - p.withdrawals
                    no_dep_equity = acc.equity - delta_deposit + delta_withdrawal

                    nav_price = invest_service.calc_nav_price(no_dep_equity, p.units_total)
                    
                    deposit_p_ids.add(p.id)
                    
                else:
                    nav_price = invest_service.calc_nav_price(acc.equity, p.units_total)
                    
                update_rows.append(p_repo._portfolio_row(p.id, acc, nav_price))
                
                if hist and hist[-1].date == today:
                    drawdown = calculate_drawdown(hist, acc.equity)
                    snapshot_rows.append(
                        p_repo._snapshot_row(p.id, today, nav_price, acc.balance, acc.equity, drawdown)
                    )
                
                gain_rows.extend(g_repo._gain_row(p.id, g) for g in gain)
            
        await p_repo.bulk_upsert(update_rows)
        await p_repo.bulk_upsert_snapshots(snapshot_rows)
        await g_repo.bulk_upsert_gains(gain_rows)
        
        if deposit_p_ids:
            await invest_service.update_batch(deposit_p_ids)
            
        await h_repo.revalue_holdings()

        logger.info(
            "MyFX sync completed: %s new / %s updates / %s snapshots / %s gains\nUpdated ids: %s",
            len(new_oids), len(update_rows), len(snapshot_rows), len(gain_rows), deposit_p_ids
        )
