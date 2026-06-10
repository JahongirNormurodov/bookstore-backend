# users/services.py
import secrets
import requests
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import User, OTPCode


def generate_otp_code() -> str:
    """Kriptografik xavfsiz 6 xonali kod"""
    return str(secrets.randbelow(900000) + 100000)


def create_otp(user: User, purpose: str) -> OTPCode:
    """Yangi OTP yaratish — eskisini bekor qilish"""

    # Avvalgi ishlatilmagan kodlarni bekor qilish
    OTPCode.objects.filter(
        user=user,
        purpose=purpose,
        is_used=False
    ).update(is_used=True)

    return OTPCode.objects.create(
        user       = user,
        code       = generate_otp_code(),
        purpose    = purpose,
        expires_at = timezone.now() + timedelta(minutes=3)
    )


def send_sms(phone: str, message: str) -> bool:
    """Eskiz.uz orqali SMS yuborish"""

    url = "https://notify.eskiz.uz/api/message/sms/send"
    headers = {
        "Authorization": f"Bearer {settings.ESKIZ_TOKEN}"  # settings dan
    }
    payload = {
        "mobile_phone": phone,
        "message":      message,
        "from":         settings.ESKIZ_SENDER,              # settings dan
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.Timeout:
        # TODO: Celery task ga o'tkazish
        raise Exception("SMS servisi vaqt limitidan oshdi.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"SMS servisi xatosi: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"SMS yuborishda xatolik: {str(e)}")


def send_verification_sms(phone: str, purpose: str) -> bool:
    """Telefonga OTP kod yuborish"""

    # User mavjudligini tekshirish
    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        raise Exception("Bu raqam ro'yxatdan o'tmagan.")

    otp = create_otp(user, purpose)

    message = (
        f"BOOKstore tasdiqlash kodi: {otp.code}. "
        f"3 daqiqa ichida kiriting. "
        f"Kodni hech kimga bermang!"
    )

    return send_sms(phone, message)

    return send_sms(phone, message)