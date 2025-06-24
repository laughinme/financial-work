from typing import Annotated
from fastapi import Depends

from core.security import auth_user, AuthRouter
from domain.dashboards import Dashboard
from service.investments import InvestmentService, get_investment_service
from database.relational_db import User


router = AuthRouter()


@router.get(
    path='/summary',
    response_model=Dashboard
)
async def dashboard_summary(
    service: Annotated[InvestmentService, Depends(get_investment_service)],
    user: Annotated[User, Depends(auth_user)]
):
    return await service.user_summary(user.id)
