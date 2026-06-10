import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel


class UserManager(BaseUserManager):
    """phone ni USERNAME_FIELD sifatida ishlatadigan manager."""
    use_in_migrations = True

    def _create_user(self, phone, email, password, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqami majburiy.")
        email = self.normalize_email(email) if email else email
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser uchun is_staff=True bo'lishi kerak.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser uchun is_superuser=True bo'lishi kerak.")
        return self._create_user(phone, email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    username = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(_("Phone"), max_length=15, unique=True)
    email = models.EmailField(_("Email"), unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

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

    @property
    def total_loyalty_points(self):
        """Foydalanuvchining umumiy balllari"""
        from django.db.models import Sum
        total = self.loyalty_points.aggregate(total=Sum('points'))['total']
        return total or 0

    @property
    def active_rentals_count(self):
        """Faol ijaralar soni"""
        return self.rentals.filter(status='active').count()

    @property
    def can_rent_more_books(self):
        """Yana kitob olish mumkinmi"""
        if self.active_plan:
            return self.active_rentals_count < self.active_plan.max_simultaneous_books
        # Obunasiz foydalanuvchilar uchun standart limit
        return self.active_rentals_count < 3


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', blank=True, null=True)
    passport_number = models.CharField(_("Passport number"), max_length=20, blank=True, null=True)
    passport_series = models.CharField(_("Passport series"), max_length=10, blank=True, null=True)
    birth_date = models.DateField(_("Birth date"), null=True, blank=True)
    address = models.TextField(_("Address"), blank=True)
    is_phone_verified = models.BooleanField(_("Phone verified"), default=False)
    is_passport_verified = models.BooleanField(_("Passport verified"), default=False)
    is_blacklisted = models.BooleanField(_("Blacklisted"), default=False)
    blacklist_reason = models.TextField(_("Blacklist reason"), blank=True)

    def __str__(self):
        return f"Profile of {self.user.phone}"
    
    @property
    def is_verified(self):
        """Foydalanuvchi to'liq tasdiqlangan"""
        return self.is_phone_verified and self.is_passport_verified


class Wishlist(TimeStampedModel):
    """Sevimli kitoblar ro'yxati"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='wishlisted_by')
    
    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")
        unique_together = ['user', 'book']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.phone} - {self.book.title}"


class SearchHistory(TimeStampedModel):
    """Qidiruv tarixi"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(_("Search query"), max_length=255)
    results_count = models.PositiveIntegerField(_("Results count"), default=0)
    
    class Meta:
        verbose_name = _("Search history")
        verbose_name_plural = _("Search histories")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.phone} - {self.query}"


class ReferralCode(TimeStampedModel):
    """Referral dasturi"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(_("Referral code"), max_length=20, unique=True)
    uses_count = models.PositiveIntegerField(_("Uses count"), default=0)
    
    class Meta:
        verbose_name = _("Referral code")
        verbose_name_plural = _("Referral codes")
    
    def __str__(self):
        return f"{self.user.phone} - {self.code}"


class Referral(TimeStampedModel):
    """Referrallar tarixi"""
    
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_by')
    reward_given = models.BooleanField(_("Reward given"), default=False)
    
    class Meta:
        verbose_name = _("Referral")
        verbose_name_plural = _("Referrals")
    
    def __str__(self):
        return f"{self.referrer.phone} -> {self.referred.phone}"


class LoyaltyPoints(TimeStampedModel):
    """Bonus ballar va cashback"""
    
    class Reason(models.TextChoices):
        RENTAL_CASHBACK = 'rental_cashback', _("Ijara cashback")
        REFERRAL_BONUS = 'referral_bonus', _("Referral bonus")
        BIRTHDAY_BONUS = 'birthday_bonus', _("Tug'ilgan kun bonusi")
        SPENT = 'spent', _("Ishlatildi")
        ADMIN_ADJUSTMENT = 'admin_adjustment', _("Admin tomonidan")
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loyalty_points')
    points = models.IntegerField(_("Points"), help_text=_("Positive = earned, negative = spent"))
    reason = models.CharField(_("Reason"), max_length=30, choices=Reason.choices)
    description = models.TextField(_("Description"), blank=True)
    
    class Meta:
        verbose_name = _("Loyalty points")
        verbose_name_plural = _("Loyalty points")
        ordering = ['-created_at']
    
    def __str__(self):
        sign = '+' if self.points > 0 else ''
        return f"{self.user.phone} | {sign}{self.points} | {self.get_reason_display()}"


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