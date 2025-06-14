from enum import Enum


class Provider(Enum):
    """Supported authentication providers."""

    PASSWORD = "password"
    TELEGRAM = "telegram"
    GOOGLE = "google"
    APPLE = "apple"
    # PHONE_OTP = "phone_otp"
