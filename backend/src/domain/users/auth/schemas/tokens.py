from pydantic import BaseModel, Field


class TokenPair(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)


class AccessToken(BaseModel):
    access_token: str = Field(...)


class RefreshToken(BaseModel):
    """Obtain access token by passing refresh."""
    
    refresh_token: str
