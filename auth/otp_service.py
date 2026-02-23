import random
import time

# In-memory OTP store (temporary for development)
otp_store = {}


def generate_otp(email: str) -> str:
    otp = str(random.randint(100000, 999999))

    otp_store[email] = {
        "otp": otp,
        "timestamp": time.time()
    }

    return otp


def validate_otp(email: str, entered_otp: str) -> bool:
    record = otp_store.get(email)

    if not record:
        return False

    # OTP valid for 5 minutes
    if time.time() - record["timestamp"] > 300:
        del otp_store[email]
        return False

    if record["otp"] == entered_otp:
        del otp_store[email]
        return True

    return False