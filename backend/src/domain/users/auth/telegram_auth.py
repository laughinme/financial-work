from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator


class TelegramAuth(BaseModel):
    id: int
    first_name: str
    last_name: str | None = Field(None)
    username: str | None = Field(None)
    photo_url: str | None = Field(None)
    auth_date: int
    hash: str

