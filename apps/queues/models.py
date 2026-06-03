# queues/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel
from apps.users.models import User
from apps.books.models import Book


class BookQueue(TimeStampedModel):
    """Kitob navbati - band kitob uchun navbatga turish"""

    class Status(models.TextChoices):
        WAITING = 'waiting', _("Kutilmoqda")
        NOTIFIED = 'notified', _("Xabar berildi")
        FULFILLED = 'fulfilled', _("Bajarildi")
        CANCELLED = 'cancelled', _("Bekor qilingan")
        EXPIRED = 'expired', _("Muddati o'tgan")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='book_queues',
        verbose_name=_("Foydalanuvchi")
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='queues',
        verbose_name=_("Kitob")
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING
    )
    position = models.PositiveIntegerField(_("Navbatdagi o'rni"), default=0)
    notified_at = models.DateTimeField(_("Xabar berilgan vaqt"), null=True, blank=True)
    expires_at = models.DateTimeField(_("Amal qilish muddati"), null=True, blank=True)
    notes = models.TextField(_("Izoh"), blank=True)

    class Meta:
        verbose_name = _("Kitob navbati")
        verbose_name_plural = _("Kitob navbatlari")
        ordering = ['created_at']  # FIFO
        unique_together = ['user', 'book', 'status']

    def __str__(self):
        return f"{self.user.phone} - {self.book.title} (#{self.position})"


class BookNotification(TimeStampedModel):
    """Kitob bo'shaganda xabar berish uchun ro'yxat"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='book_notifications',
        verbose_name=_("Foydalanuvchi")
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='notification_requests',
        verbose_name=_("Kitob")
    )
    is_notified = models.BooleanField(_("Xabar berildi"), default=False)
    notified_at = models.DateTimeField(_("Xabar berilgan vaqt"), null=True, blank=True)

    class Meta:
        verbose_name = _("Kitob xabarnomasi")
        verbose_name_plural = _("Kitob xabarnomalar")
        ordering = ['created_at']
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.user.phone} - {self.book.title}"
