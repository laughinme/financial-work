from pydantic import BaseModel, Field
from uuid import UUID


class UserSchema(BaseModel):
    """Minimal user profile data."""

    id: UUID = Field(..., description="User identifier")
    
    display_name: str| None = Field(None)
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    avatar_url: str | None = Field(None)
    banned: bool = Field(...)
