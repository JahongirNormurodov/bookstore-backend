import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    username = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(_("Phone"), max_length=15, unique=True)
    email = models.EmailField(_("Email"), unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.phone} - {self.first_name or ''}"

    @property
    def current_trust_score(self):
        score = self.trust_scores.order_by('-created_at').first()
        return score.score if score else 100

    @property
    def active_plan(self):
        active_sub = self.subscriptions.filter(status='active').first()
        return active_sub.plan if active_sub else None


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', blank=True, null=True)
    passport_number = models.CharField(_("Passport number"), max_length=20, blank=True, null=True)
    birth_date = models.DateField(_("Birth date"), null=True, blank=True)
    address = models.TextField(_("Address"), blank=True)
    is_phone_verified = models.BooleanField(_("Phone verified"), default=False)
    is_passport_verified = models.BooleanField(_("Passport verified"), default=False)

    def __str__(self):
        return f"Profile of {self.user.phone}"


class TrustScore(TimeStampedModel):
    class Reason(models.TextChoices):
        BOOK_RETURNED_LATE = 'late_return', _("Book returned late")
        BOOK_DAMAGED = 'book_damaged', _("Book returned damaged")
        BOOK_LOST = 'book_lost', _("Book lost")
        PASSPORT_VERIFIED = 'passport_verified', _("Passport verified")
        GOOD_BEHAVIOR = 'good_behavior', _("Good behavior")
        MANUAL_ADJUSTMENT = 'manual', _("Manual adjustment by admin")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trust_scores')
    score = models.SmallIntegerField(
        _("Score change"),
        help_text=_("Positive = bonus, negative = penalty. E.g. -10, +5")
    )
    reason = models.CharField(_("Reason"), max_length=30, choices=Reason.choices)
    comment = models.TextField(_("Comment"), blank=True)
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='trust_adjustments',
        help_text=_("Admin who made the change, null if system")
    )

    class Meta:
        verbose_name = _("Trust score")
        verbose_name_plural = _("Trust scores")
        ordering = ['-created_at']

    def __str__(self):
        sign = '+' if self.score > 0 else ''
        return f"{self.user.phone} | {sign}{self.score} | {self.get_reason_display()}"


# users/models.py
class OTPCode(TimeStampedModel):
    """SMS tasdiqlash kodlari"""

    class Purpose(models.TextChoices):
        REGISTER      = 'register',       _("Ro'yxatdan o'tish")
        LOGIN         = 'login',          _("Kirish")
        RESET_PASSWORD = 'reset_password', _("Parol tiklash")

    user       = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='otp_codes',
        verbose_name=_("Foydalanuvchi")
    )
    code       = models.CharField(_("Kod"), max_length=6)
    purpose    = models.CharField(_("Maqsad"), max_length=20, choices=Purpose.choices)
    is_used    = models.BooleanField(_("Ishlatilgan"), default=False)
    expires_at = models.DateTimeField(_("Amal qilish muddati"))

    class Meta:
        verbose_name        = _("OTP kod")
        verbose_name_plural = _("OTP kodlar")
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.user.phone} - {self.code} ({self.get_purpose_display()})"

    @property
    def is_expired(self):
        from django.utils.timezone import now
        return now() > self.expires_at

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired

    def verify(self):
        """Kodni ishlatilgan deb belgilash"""
        self.is_used = True
        self.save(update_fields=['is_used'])