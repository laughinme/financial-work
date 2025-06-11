from typing import Annotated
from fastapi import APIRouter, Depends, Path

from domain.investments import InvestSchema
from core.security import auth_user
from service.investments import InvestmentService, get_investment_service
from database.relational_db import User


router = APIRouter()


@router.post(
    path='/invest',
    status_code=204
)
async def invest_in_portfolio(
    payload: InvestSchema,
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    service: InvestmentService = Depends(get_investment_service),
    user: User = Depends(auth_user)
):
    await service.invest(portfolio_id, payload.amount, user.id)
