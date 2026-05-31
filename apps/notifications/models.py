# notifications/models.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel
from apps.users.models import User
from apps.notifications.choices import NotificationType


class Notification(TimeStampedModel):
    """Bildirishnomalar"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_("Foydalanuvchi")
    )
    notification_type = models.CharField(
        _("Turi"),
        max_length=30,
        choices=NotificationType.choices
    )

    title   = models.CharField(_("Sarlavha"), max_length=200)
    message = models.TextField(_("Matn"))

    is_read = models.BooleanField(_("O'qilgan"), default=False)
    read_at = models.DateTimeField(_("O'qilgan vaqt"), null=True, blank=True)

    # Bog'liq obyektlar — barchasi optional
    related_rental = models.ForeignKey(
        'rentals.Rental',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='notifications',
        verbose_name=_("Bog'liq ijara")
    )
    related_book = models.ForeignKey(
        'books.Book',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='notifications',
        verbose_name=_("Bog'liq kitob")
    )

    class Meta:
        verbose_name        = _("Bildirishnoma")
        verbose_name_plural = _("Bildirishnomalar")
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.user.phone} - {self.title[:50]}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
