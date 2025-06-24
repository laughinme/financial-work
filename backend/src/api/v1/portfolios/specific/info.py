from typing import Annotated
from fastapi import Depends, Path

from core.security import auth_user, AuthRouter
from domain.investments import PortfolioOverview
from service.portfolios import PortfolioService, get_portfolio_service
from database.relational_db import User


router = AuthRouter()


@router.get(
    path='/',
    response_model=PortfolioOverview,
    responses={404: {"description": "Portfolio not found"}}
)
async def get_specific_portfolio(
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    portfolio_service: Annotated[PortfolioService, Depends(get_portfolio_service)],
    user: Annotated[User, Depends(auth_user)]
):
    portfolio = await portfolio_service.get_specific(user.id, portfolio_id)
    return portfolio
