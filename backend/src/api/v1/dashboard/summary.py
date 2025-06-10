from fastapi import APIRouter, Depends, Query

from core.security import auth_user
from domain.users import DashboardSchema
from service.investments import InvestmentService, get_investment_service
from database.relational_db import User


router = APIRouter()


@router.get(
    path='/summary',
    response_model=DashboardSchema
)
async def dashboard_summary(
    service: InvestmentService = Depends(get_investment_service),
    user: User = Depends(auth_user)
):
    return await service.user_summary(user.id)
