import pyotp


class OTPGenerator:
    issuer_name = "Financial porno"

    async def generate_2fa_otp(self, secret: str, username: str):
        totp = pyotp.TOTP(secret)
        otp_uri = totp.provisioning_uri(name=username, issuer_name=self.issuer_name)
        return otp_uri

    @staticmethod
    async def generate_secret():
        return pyotp.random_base32()
