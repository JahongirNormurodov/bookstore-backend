# common/settings_model.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache


class SystemSettings(models.Model):
    """Tizim sozlamalari - singleton pattern"""
    
    # Ijara sozlamalari
    default_rental_daily_rate = models.DecimalField(
        _("Kunlik ijara foizi"),
        max_digits=5,
        decimal_places=4,
        default=0.01,
        help_text=_("Kitob narxidan foiz (0.01 = 1%)")
    )
    default_rental_weekly_rate = models.DecimalField(
        _("Haftalik ijara foizi"),
        max_digits=5,
        decimal_places=4,
        default=0.05
    )
    default_rental_monthly_rate = models.DecimalField(
        _("Oylik ijara foizi"),
        max_digits=5,
        decimal_places=4,
        default=0.15
    )
    
    max_rental_days = models.PositiveIntegerField(
        _("Maksimal ijara muddati (kun)"),
        default=60
    )
    max_simultaneous_rentals = models.PositiveIntegerField(
        _("Bir vaqtda maksimal kitoblar soni"),
        default=3
    )
    max_extension_count = models.PositiveIntegerField(
        _("Maksimal uzaytirish soni"),
        default=2
    )
    
    # Jarima sozlamalari
    penalty_per_day = models.DecimalField(
        _("Kunlik jarima"),
        max_digits=10,
        decimal_places=2,
        default=5000.00
    )
    penalty_grace_days = models.PositiveIntegerField(
        _("Grace period (kunlar)"),
        default=0,
        help_text=_("Kechikish uchun jarima boshlanishidan oldin")
    )
    max_overdue_days_before_full_charge = models.PositiveIntegerField(
        _("To'liq garov ushlab qolinishidan oldingi kunlar"),
        default=30
    )
    
    # Bildirishnoma sozlamalari
    notification_due_3_days = models.BooleanField(_("3 kun oldin eslatma"), default=True)
    notification_due_1_day = models.BooleanField(_("1 kun oldin eslatma"), default=True)
    notification_overdue = models.BooleanField(_("Kechikkan xabar"), default=True)
    
    # Ishonchlilik sozlamalari
    initial_trust_score = models.PositiveIntegerField(_("Boshlang'ich trust score"), default=100)
    min_trust_score = models.SmallIntegerField(_("Minimal trust score"), default=0)
    max_trust_score = models.PositiveIntegerField(_("Maksimal trust score"), default=200)
    
    # Trust score o'zgarishlari
    trust_score_late_return_penalty = models.SmallIntegerField(_("Kech qaytarish jazosi"), default=-10)
    trust_score_on_time_bonus = models.SmallIntegerField(_("O'z vaqtida qaytarish bonusi"), default=5)
    trust_score_book_lost_penalty = models.SmallIntegerField(_("Kitob yo'qolgan jazosi"), default=-50)
    trust_score_book_damaged_penalty = models.SmallIntegerField(_("Kitob shikastlangan jazosi"), default=-20)
    
    # Cashback va bonus
    cashback_percentage = models.DecimalField(
        _("Cashback foizi"),
        max_digits=5,
        decimal_places=2,
        default=5.00
    )
    referral_bonus_points = models.PositiveIntegerField(_("Referral bonus ballari"), default=10000)
    birthday_bonus_points = models.PositiveIntegerField(_("Tug'ilgan kun bonusi"), default=5000)
    
    # Boshqa
    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Yangilangan"), auto_now=True)
    
    class Meta:
        verbose_name = _("Tizim sozlamalari")
        verbose_name_plural = _("Tizim sozlamalari")
    
    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton pattern
        super().save(*args, **kwargs)
        cache.delete('system_settings')  # Clear cache
    
    def delete(self, *args, **kwargs):
        pass  # Prevent deletion
    
    @classmethod
    def load(cls):
        """Get or create settings"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
    
    def __str__(self):
        return "Tizim sozlamalari"
