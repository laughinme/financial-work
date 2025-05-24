from enum import Enum


class Provider(Enum):
    """Different oauth providers."""
    CREDENTIALS = "credentials"
    TELEGRAM = "telegram"
    GOOGLE = "google"
