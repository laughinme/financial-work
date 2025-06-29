from pydantic import BaseModel, Field, EmailStr


class LinkEmail(BaseModel):
    """Schema used to link email to account"""
    
    email: EmailStr = Field(...)


class LinkPhone(BaseModel):
    """Schema used to link phone number to account"""
    
    phone: str = Field(...)
