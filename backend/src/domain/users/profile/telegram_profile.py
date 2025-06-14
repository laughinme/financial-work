from pydantic import BaseModel, Field
from uuid import UUID


class TelegramUserSchema(BaseModel):
    """Telegram profile linked to a user."""

    id: int = Field(..., description="Telegram user identifier")
    first_name: str = Field(..., description="Telegram first name")
    last_name: str | None = Field(None, description="Telegram last name")
    username: str | None = Field(None, description="Telegram username")
    photo_url: str | None = Field(None, description="Avatar URL from Telegram")
