# subscriptions/choices.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionStatus(models.TextChoices):
    ACTIVE    = 'active',    _("Faol")
    EXPIRED   = 'expired',   _("Muddati tugagan")
    CANCELLED = 'cancelled', _("Bekor qilingan")
    PENDING   = 'pending',   _("Kutilmoqda")