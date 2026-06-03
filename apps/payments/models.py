# payments/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel
from apps.users.models import User
from apps.rentals.models import Rental
from apps.subscriptions.models import Subscription


class Payment(TimeStampedModel):
    """To'lovlar"""

    class PaymentType(models.TextChoices):
        RENTAL = 'rental', _("Ijara to'lovi")
        DEPOSIT = 'deposit', _("Garov")
        PENALTY = 'penalty', _("Jarima")
        SUBSCRIPTION = 'subscription', _("Obuna to'lovi")
        REFUND = 'refund', _("Qaytarish")

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', _("Naqd")
        CARD = 'card', _("Karta")
        PAYME = 'payme', _("Payme")
        CLICK = 'click', _("Click")
        UZUM = 'uzum', _("Uzum")

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', _("Kutilmoqda")
        COMPLETED = 'completed', _("To'langan")
        FAILED = 'failed', _("Muvaffaqiyatsiz")
        REFUNDED = 'refunded', _("Qaytarilgan")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_("Foydalanuvchi")
    )
    amount = models.DecimalField(_("Summa"), max_digits=12, decimal_places=2)
    payment_type = models.CharField(_("To'lov turi"), max_length=20, choices=PaymentType.choices)
    payment_method = models.CharField(_("To'lov usuli"), max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(_("Status"), max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    # Bog'liq obyektlar
    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='payments',
        verbose_name=_("Ijara")
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='payments',
        verbose_name=_("Obuna")
    )

    transaction_id = models.CharField(_("Tranzaksiya ID"), max_length=255, blank=True)
    description = models.TextField(_("Tavsif"), blank=True)
    notes = models.TextField(_("Izohlar"), blank=True)

    class Meta:
        verbose_name = _("To'lov")
        verbose_name_plural = _("To'lovlar")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_id']),
        ]

    def __str__(self):
        return f"{self.user.phone} - {self.amount} - {self.get_payment_type_display()}"


class Penalty(TimeStampedModel):
    """Kech qaytarish jarimalari"""

    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        related_name='penalties',
        verbose_name=_("Ijara")
    )
    days_overdue = models.PositiveIntegerField(_("Kechikkan kunlar"))
    penalty_amount = models.DecimalField(_("Jarima summasi"), max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(_("To'langan"), default=False)
    paid_at = models.DateTimeField(_("To'langan vaqt"), null=True, blank=True)
    notes = models.TextField(_("Izoh"), blank=True)

    class Meta:
        verbose_name = _("Jarima")
        verbose_name_plural = _("Jarimalar")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rental} - {self.penalty_amount} ({self.days_overdue} kun)"
