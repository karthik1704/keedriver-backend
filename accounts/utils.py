# utils.py
import base64

import pyotp
import requests
from django.conf import settings
from django.http import JsonResponse


def send_whatsapp_message(phone_number, message):
    """Send a WhatsApp message using WhatsApp Business API."""
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,  # E.g., "919876543210" (without '+' sign)
        "type": "text",
        "text": {
            "body": message,
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def generate_totp(phone_number):
    """Generate a TOTP with a 2-minute expiry based on a secret key and user's phone number."""

    base32_secret = base64.b32encode(
        f"{settings.TOTP_SECRET_KEY}{phone_number}".encode("utf-8")
    ).decode("utf-8")

    totp = pyotp.TOTP(
        base32_secret,
        interval=settings.TOTP_INTERVAL,
    )
    return totp.now()  # Generate the current OTP


def verify_totp(phone_number, otp):
    """Verify the TOTP with a 2-minute expiry based on the secret key and user's phone number."""
    base32_secret = base64.b32encode(
        f"{settings.TOTP_SECRET_KEY}{phone_number}".encode("utf-8")
    ).decode("utf-8")

    totp = pyotp.TOTP(base32_secret, interval=settings.TOTP_INTERVAL)
    return totp.verify(otp)  # Returns True if OTP is valid


def send_otp(phone_number):
    """Send the TOTP to the user's phone number."""
    # Generate OTP
    otp = generate_totp(phone_number)
    message = f"Your OTP code is {otp}. It will expire in 2 minutes."
    print(otp)
    # Send OTP to the phone number
    # try:
    #     res = send_whatsapp_message(phone_number, message=message)
    #     return otp, True

    # except Exception as e:
    #     print(e)
    #     return JsonResponse({"error": str(e)}, status=500)
    return otp, True
