from django.utils.translation import gettext_lazy as _
from django.db import models


class RentalStatus(models.TextChoices):
    PENDING = 'pending', _("Kutilmoqda")
    ACTIVE = 'active', _("Faol")
    OVERDUE = 'overdue', _("Muddati o‘tgan")
    RETURNED = 'returned', _("Qaytarilgan")
    CANCELLED = 'cancelled', _("Bekor qilingan")


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', _('Kutilmoqda')
    PAID = 'paid', _('To‘langan')
    UNPAID = 'unpaid', _('To‘lanmagan')
    PARTIALLY_PAID = 'partially_paid', _('Qisman to‘langan')
    REFUNDED = 'refunded', _('Qaytarilgan')
    