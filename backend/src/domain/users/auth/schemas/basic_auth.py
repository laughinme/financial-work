from typing_extensions import Self
from pydantic import BaseModel, Field, EmailStr, model_validator


class UserRegister(BaseModel):
    """Data required for user registration."""

    email: EmailStr | None = Field(None, description="User e-mail")
    phone_number: str | None = Field(None, description="User phone number")

    password: str = Field(..., description="User password")
    # secret: str = Field(...)
    
    @model_validator(mode='after')
    def validator(self) -> Self:
        if self.email is None and self.phone_number is None:
            raise ValueError('Either a telephone number or an email address must be provided')
        return self
    

class UserLogin(BaseModel):
    """Credentials used for user login."""

    email: EmailStr | None = Field(None, description="User e-mail")
    phone_number: str | None = Field(None, description="User phone number")

    password: str = Field(..., description='User password')
    # secret: str = Field(...)
