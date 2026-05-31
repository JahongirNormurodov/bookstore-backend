# subscriptions/models.py
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel
from apps.users.models import User
from apps.subscriptions.choices import SubscriptionStatus


class SubscriptionPlan(TimeStampedModel):
    """Obuna tariflari"""

    name  = models.CharField(_("Tarif nomi"), max_length=100)
    slug  = models.SlugField(unique=True)
    price_monthly = models.DecimalField(_("Oylik narx"), max_digits=10, decimal_places=2)

    max_books_per_month     = models.PositiveIntegerField(_("Oylik kitob limiti"), default=2)
    max_simultaneous_books  = models.PositiveIntegerField(_("Bir vaqtda nechta kitob"), default=1)
    is_unlimited            = models.BooleanField(_("Cheksiz"), default=False)

    description = models.TextField(_("Tavsif"), blank=True)
    is_active   = models.BooleanField(_("Faol"), default=True)

    class Meta:
        verbose_name        = _("Obuna tarifi")
        verbose_name_plural = _("Obuna tariflari")
        ordering            = ['price_monthly']

    def __str__(self):
        return self.name


class Subscription(TimeStampedModel):
    """Foydalanuvchining obunasi"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name=_("Foydalanuvchi")
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name=_("Tarif")
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.PENDING
    )

    start_date   = models.DateField(_("Boshlanish sanasi"))
    end_date     = models.DateField(_("Tugash sanasi"))
    cancelled_at = models.DateTimeField(_("Bekor qilingan sana"), null=True, blank=True)

    auto_renew = models.BooleanField(_("Avto yangilanish"), default=True)
    notes      = models.TextField(_("Eslatmalar"), blank=True)

    class Meta:
        verbose_name        = _("Obuna")
        verbose_name_plural = _("Obunalar")
        ordering            = ['-created_at']
        constraints         = [
            # Bir userda bir vaqtda faqat bitta ACTIVE obuna
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(status='active'),
                name='unique_active_subscription_per_user'
            )
        ]

    def __str__(self):
        return f"{self.user.phone} - {self.plan.name}"

    @property
    def is_expired(self):
        return self.end_date < now().date()

    def cancel(self):
        self.status       = SubscriptionStatus.CANCELLED
        self.cancelled_at = now()
        self.auto_renew   = False
        self.save(update_fields=['status', 'cancelled_at', 'auto_renew'])