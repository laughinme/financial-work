from typing import Annotated
from fastapi import Depends, Path

from domain.investments import WithdrawSchema
from core.security import auth_user, AuthRouter
from service.investments import InvestmentService, get_investment_service
from database.relational_db import User


router = AuthRouter()


@router.post(
    path='/withdraw',
    status_code=204,
    responses={
        404: {"description": "Portfolio with this id not found"},
        402: {"description": "It can be either insufficient funds or incorrect currency"}
    }
)
async def withdraw_from_portfolio(
    payload: WithdrawSchema,
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    service: Annotated[InvestmentService, Depends(get_investment_service)],
    user: Annotated[User, Depends(auth_user)]
):
    await service.withdraw(portfolio_id, payload.units, user.id)
