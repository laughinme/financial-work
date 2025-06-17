from typing import Annotated
from fastapi import Depends, Query

from core.security import auth_user, AuthRouter
from domain.dashboards import AllocationPie, PortfolioValue, DailyPnl
from service.dashboard import DashboardService, get_dashboard_service
from database.relational_db import User


router = AuthRouter()


@router.get(
    path='/allocation',
    response_model=list[AllocationPie]
)
async def allocation_pie(
    service: Annotated[DashboardService, Depends(get_dashboard_service)],
    user: Annotated[User, Depends(auth_user)]
):
    return await service.allocation(user.id)


@router.get(
    path="/daily-pnl",
    response_model=list[DailyPnl]
)
async def daily_pnl(
    service: Annotated[DashboardService, Depends(get_dashboard_service)],
    user: Annotated[User, Depends(auth_user)],
    days: int = Query(90, ge=1, le=365, description='Chart chronological period'),
):
    return await service.daily_pnl(user.id, days)


@router.get(
    path='/portfolio-value',
    response_model=list[PortfolioValue]
)
async def portfolio_value(
    service: Annotated[DashboardService, Depends(get_dashboard_service)],
    user: Annotated[User, Depends(auth_user)],
    days: int = Query(90, ge=1, le=365, description='Chart chronological period'),
):
    return await service.portfolio_value(user.id, days)
