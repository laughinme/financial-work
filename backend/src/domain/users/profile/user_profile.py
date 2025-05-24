from pydantic import BaseModel, Field
from uuid import UUID


class UserSchema(BaseModel):
    id: UUID
    email: str | None
    phone_number: str | None
