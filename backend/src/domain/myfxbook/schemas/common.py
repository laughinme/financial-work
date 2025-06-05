from pydantic import BaseModel


class CommonModel(BaseModel):
    """Common fields for all MyFXbook API responses"""
    error: bool
    message: str
