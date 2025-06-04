from typing import Annotated
from fastapi import APIRouter, Depends, Path

from core.security import auth_user
from domain.investments import PortfolioOverview
from service.portfolios import PortfolioService, get_portfolio_service
from database.relational_db import User


router = APIRouter()


@router.get(
    path='/',
    response_model=PortfolioOverview
)
async def get_specific_portfolio(
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    _: User = Depends(auth_user)
):
    portfolio = await portfolio_service.get_specific(portfolio_id)
    return portfolio
