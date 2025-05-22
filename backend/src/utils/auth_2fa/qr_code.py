import asyncio

import qrcode

from .otp_generator import OTPGenerator


class QRCodeGenerator2FA:
    @staticmethod
    async def create_qr(secret: str, username: str):
        qr_image = await asyncio.to_thread(qrcode.make, await OTPGenerator().generate_2fa_otp(secret, username))
        qr_image.save("test.png")
