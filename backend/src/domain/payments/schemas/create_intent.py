from typing import Self
from pydantic import BaseModel, Field, model_validator
from decimal import Decimal

from ..enums import DepositAction


class CreatePayment(BaseModel):
    amount: Decimal = Field(..., description='Required payment amount in double format (100.00)')
    currency: str = Field(
        'USD', description='Only USD is allowed'
    )
    description: str | None = Field(
        None, description='For example: “Payment for order #72 for user@example.com”.'
    )
    
    action: DepositAction = Field(
        DepositAction.DEPOSIT, 
        description = 'For one-click payments you can choose an action and provide action_id.' \
                      'By default it is deposit to internal wallet'
    )
    action_id: str | None = Field(
        None, description='Id of object payment is for, e.g. portfolio_id. Required if action != "deposit"'
    )
    
    success_url: str = Field(..., description='User will be redirected to this url on success')
    cancel_url: str = Field(..., description='User will be redirected to this url on payment cancel')
    
    @model_validator(mode='after')
    def check_action(self) -> Self:
        if self.action != DepositAction.DEPOSIT and self.action_id is None:
            raise ValueError(f'Action mode {self.action} requires action_id field to be passed')
        if self.currency != 'USD':
            raise ValueError('Only USD is allowed')
        return self


class CreatePayout(BaseModel):
    amount: Decimal = Field(..., description='Amount of funds to withdraw in USD')
