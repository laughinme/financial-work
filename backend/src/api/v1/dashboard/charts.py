from typing import Annotated
from fastapi import Depends, Query

from core.security import auth_user, AuthRouter
from domain.dashboards import AllocationPie, CashFlow
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
    path='/cashflow',
    response_model=list[CashFlow]
)
async def cashflow(
    service: Annotated[DashboardService, Depends(get_dashboard_service)],
    user: Annotated[User, Depends(auth_user)],
    days: int = Query(90, ge=1, le=365, description='Chart chronological period'),
):
    return await service.cashflow(user.id, days)
