from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class TelegramAuthSchema(BaseModel):
    """Data sent by Telegram login widget."""

    id: int = Field(..., description="Telegram user identifier")
    first_name: str = Field(..., description="First name of the user")
    last_name: str | None = Field(None, description="Last name of the user")
    username: str | None = Field(None, description="Telegram username")
    photo_url: str | None = Field(None, description="URL to the user's avatar")
    auth_date: datetime = Field(..., description="Authorization timestamp")
    hash: str = Field(..., description="Telegram signature hash")
