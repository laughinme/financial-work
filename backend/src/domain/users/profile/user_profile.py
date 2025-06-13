from pydantic import BaseModel, Field
from uuid import UUID


class UserSchema(BaseModel):
    """Minimal user profile data."""

    id: UUID = Field(..., description="User identifier")
