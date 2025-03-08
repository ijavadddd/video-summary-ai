import email
import base64
import pyotp
from accounts.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models import Q


def generate_otp(username_email: str):
    user = User.objects.get(Q(username=username_email) | Q(email=username_email))

    # Create a seed using user-specific fields and the secret key
    seed = f"{user.email}-{user.username}-{settings.SECRET_KEY}"

    # Encode the seed in base32
    base32_seed = base64.b32encode(seed.encode()).decode()

    # Create a TOTP object using the base32-encoded seed
    totp = pyotp.TOTP(base32_seed, interval=60)  # 1-minute interval

    # Generate the OTP
    otp = totp.at(timezone.now().timestamp())
    return otp
