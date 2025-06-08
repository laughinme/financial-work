from typing import Annotated
from fastapi import APIRouter, Depends, Path

from core.security import auth_user
from domain.investments import UserHolding
from service.investments import InvestmentService, get_investment_service
from database.relational_db import User


router = APIRouter()


@router.get(
    path='/user_holding',
    response_model=UserHolding
)
async def user_holding(
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    service: InvestmentService = Depends(get_investment_service),
    user: User = Depends(auth_user)
):
    holding = await service.user_portfolio(user.id, portfolio_id)
    return holding
