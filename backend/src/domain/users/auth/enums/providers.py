from enum import Enum


class Provider(Enum):
    """Supported authentication providers."""

    TELEGRAM = "telegram"
    GOOGLE = "google"
    APPLE = "apple"
    # PHONE_OTP = "phone_otp"
