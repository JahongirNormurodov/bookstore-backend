# notifications/choices.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):
    RENTAL_REMINDER      = 'rental_reminder',      _("Ijara eslatmasi")
    RENTAL_DUE_SOON      = 'rental_due_soon',      _("Qaytarish muddati yaqin")
    OVERDUE              = 'overdue',              _("Muddati o'tgan")
    RETURN_SUCCESS       = 'return_success',       _("Kitob qaytarildi")
    DEPOSIT_RETURNED     = 'deposit_returned',     _("Garov qaytarildi")
    NEW_BOOK             = 'new_book',             _("Yangi kitob")
    BOOK_AVAILABLE       = 'book_available',       _("Kitob bo'shadi")
    QUEUE_AVAILABLE      = 'queue_available',      _("Navbatdagi kitob bo'shadi")
    SUBSCRIPTION_EXPIRY  = 'subscription_expiry',  _("Obuna tugayapti")
    PENALTY_APPLIED      = 'penalty_applied',      _("Jarima qo'llanildi")
    EXTENSION_APPROVED   = 'extension_approved',   _("Uzaytirish tasdiqlandi")