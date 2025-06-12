import logging
import pyotp
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OTPGenerator:
    """
    A class to manage Time-based One-Time Passwords (TOTP) for 2FA.

    Attributes:
        issuer_name (str): The name of the application or service issuing the OTPs.
    """

    issuer_name: str = "Financial project"

    def __init__(self, issuer_name: Optional[str] = None):
        """
        Initialize the OTPGenerator.

        Args:
            issuer_name (Optional[str]): Optionally override the default issuer name.
        """
        if issuer_name:
            self.issuer_name = issuer_name
        logger.debug(f"OTPGenerator initialized with issuer: {self.issuer_name}")

    async def generate_2fa_otp(self, secret: str, username: str) -> str:
        """
        Generate a provisioning URI that can be scanned by an authenticator app.

        Args:
            secret (str): The shared secret key for generating the OTP.
            username (str): The user's identifier (typically email or username).

        Returns:
            str: A provisioning URI for use with apps like Google Authenticator.
        """
        logger.info(f"Generating OTP URI for user: {username}")
        totp = pyotp.TOTP(secret)
        otp_uri = totp.provisioning_uri(name=username, issuer_name=self.issuer_name)
        logger.debug(f"OTP URI generated: {otp_uri}")
        return otp_uri

    @staticmethod
    async def generate_secret(length: int = 32) -> str:
        """
        Generate a new random base32-encoded secret for TOTP.

        Args:
            length (int): Desired length of the secret (default: 32).

        Returns:
            str: A base32-encoded secret suitable for TOTP.
        """
        logger.info(f"Generating new secret with length: {length}")
        secret = pyotp.random_base32(length=length)
        logger.debug(f"Secret generated: {secret}")
        return secret

    @staticmethod
    def verify_otp(secret: str, otp_code: str, valid_window: int = 1) -> bool:
        """
        Verify a given TOTP code against the current time window.

        Args:
            secret (str): The shared secret key.
            otp_code (str): The OTP code to verify.
            valid_window (int): Number of time steps before or after the current time to allow.

        Returns:
            bool: True if valid, False otherwise.
        """
        logger.info("Verifying OTP code.")
        totp = pyotp.TOTP(secret)
        result = totp.verify(otp_code, valid_window=valid_window)
        logger.debug(f"OTP verification result: {result}")
        return result


# Example usage (for local testing/debugging only):
# import asyncio
# async def main():
#     generator = OTPGenerator()
#     secret = await generator.generate_secret()
#     print("Secret:", secret)
#     otp_uri = await generator.generate_2fa_otp(secret, "user@example.com")
#     print("Provisioning URI:", otp_uri)
# asyncio.run(main())
