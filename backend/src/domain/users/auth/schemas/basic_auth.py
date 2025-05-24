from typing_extensions import Self
from pydantic import BaseModel, Field, EmailStr, model_validator


class UserRegister(BaseModel):
    email: EmailStr | None = Field(None)
    phone_number: str | None = Field(None)
    
    password: str = Field(...)
    # secret: str = Field(...)
    
    @model_validator(mode='after')
    def validator(self) -> Self:
        if self.email is None and self.phone_number is None:
            raise ValueError('Either a telephone number or an email address must be provided')
        return self
    

class UserLogin(BaseModel):
    email: EmailStr | None = Field(None)
    phone_number: str | None = Field(None)

    password: str = Field(...)
    # secret: str = Field(...)
