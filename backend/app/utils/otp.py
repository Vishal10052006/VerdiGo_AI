import random

from app.config.settings import settings


def generate_otp() -> str:
    otp = "".join(
        random.choices(
            "0123456789",
            k=settings.OTP_LENGTH
        )
    )

    return otp

def validate_otp(otp: str) -> bool:

    if len(otp) != settings.OTP_LENGTH:
        return False

    if not otp.isdigit():
        return False

    return True