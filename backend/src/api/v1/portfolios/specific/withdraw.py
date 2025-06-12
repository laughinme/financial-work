from typing import Annotated
from fastapi import APIRouter, Depends, Path

from domain.investments import WithdrawSchema
from core.security import auth_user
from service.investments import InvestmentService, get_investment_service
from database.relational_db import User


router = APIRouter()


@router.post(
    path='/withdraw',
    status_code=204
)
async def withdraw_from_portfolio(
    payload: WithdrawSchema,
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    service: Annotated[InvestmentService, Depends(get_investment_service)],
    user: Annotated[User, Depends(auth_user)]
):
    await service.withdraw(portfolio_id, payload.amount, user.id)
