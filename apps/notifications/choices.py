# notifications/choices.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):
    RENTAL_REMINDER      = 'rental_reminder',      _("Ijara eslatmasi")
    OVERDUE              = 'overdue',               _("Muddati o'tgan")
    RETURN_SUCCESS       = 'return_success',        _("Kitob qaytarildi")
    NEW_BOOK             = 'new_book',              _("Yangi kitob")
    QUEUE_AVAILABLE      = 'queue_available',       _("Navbatdagi kitob bo'shadi")
    SUBSCRIPTION_EXPIRY  = 'subscription_expiry',  _("Obuna tugayapti")