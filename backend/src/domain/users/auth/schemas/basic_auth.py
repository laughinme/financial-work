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
        """Require exactly one identifier (email or phone)."""
        if (self.email is None) == (self.phone_number is None):
            raise ValueError(
                'Either telephone number or email must be provided, but not both'
            )
        return self
    

class UserLogin(BaseModel):
    """Credentials used for user login."""

    email: EmailStr | None = Field(None, description="User e-mail")
    phone_number: str | None = Field(None, description="User phone number")

    password: str = Field(..., description='User password')
    # secret: str = Field(...)
    
    
class LinkEmail(BaseModel):
    """Schema used to link email to account"""
    
    email: EmailStr = Field(...)


class LinkPhone(BaseModel):
    """Schema used to link phone number to account"""
    
    phone: str = Field(...)
