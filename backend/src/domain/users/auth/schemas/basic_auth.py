from pydantic import BaseModel, Field, EmailStr


class UserRegister(BaseModel):
    """Data required for user registration."""

    email: EmailStr | None = Field(None, description="User email")
    password: str = Field(..., description="User password")
    

class UserLogin(BaseModel):
    """Credentials used for user login."""

    email: EmailStr | None = Field(None, description="User email")
    password: str = Field(..., description='User password')
