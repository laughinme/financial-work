from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException

from core.security import auth_user, AuthRouter
from domain.investments import UserHolding
from service.investments import InvestmentService, get_investment_service
from database.relational_db import User


router = AuthRouter()


@router.get(
    path='/user-holding',
    response_model=UserHolding,
    responses={
        404: {"description": "No holdings found for this user and portfolio"}
    }
)
async def user_holding(
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    service: InvestmentService = Depends(get_investment_service),
    user: User = Depends(auth_user)
):
    holding = await service.user_portfolio(user.id, portfolio_id)
    if holding is None:
        raise HTTPException(404, detail='No holdings found for this user and portfolio')
        
    return holding


@router.get(
    path='/user_holding',
    response_model=UserHolding,
    responses={
        404: {"description": "No holdings found for this user and portfolio"}
    },
    deprecated=True
)
async def user_holding(
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    service: InvestmentService = Depends(get_investment_service),
    user: User = Depends(auth_user)
):
    holding = await service.user_portfolio(user.id, portfolio_id)
    if holding is None:
        raise HTTPException(404, detail='No holdings found for this user and portfolio')
        
    return holding
