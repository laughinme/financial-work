from pydantic import BaseModel, Field
from uuid import UUID


class TelegramUserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = Field(None)
    username: str | None = Field(None)
    photo_url: str | None = Field(None)
