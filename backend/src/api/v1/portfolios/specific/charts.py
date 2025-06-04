from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path

from core.security import auth_user
from domain.investments import PortfolioCharts
from service.portfolios import PortfolioService, get_portfolio_service
from database.relational_db import User


router = APIRouter()


@router.get(
    path='/history',
    response_model=PortfolioCharts
)
async def get_portfolio_history(
    portfolio_id: Annotated[int, Path(..., description='Portfolio id')],
    days: int = Query(30, ge=3, description='Period in days for which to display data'),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    _: User = Depends(auth_user)
):
    history = await portfolio_service.get_history(portfolio_id, days)
    return history
