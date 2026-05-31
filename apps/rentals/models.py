# rentals/models.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel
from apps.users.models import User
from apps.books.models import BookCopy
from apps.rentals.choices import RentalStatus


class Rental(TimeStampedModel):
    """Kitob ijarasi"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rentals',
        verbose_name=_("Foydalanuvchi")
    )
    book_copy = models.ForeignKey(
        BookCopy,
        on_delete=models.CASCADE,
        related_name='rentals',
        verbose_name=_("Kitob nusxasi")
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=RentalStatus.choices,
        default=RentalStatus.PENDING
    )

    rented_at    = models.DateTimeField(_("Ijaraga olingan sana"), null=True, blank=True)
    due_date     = models.DateField(_("Qaytarish muddati"))
    returned_at  = models.DateTimeField(_("Qaytarilgan sana"), null=True, blank=True)

    rental_price   = models.DecimalField(_("Ijara narxi"), max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(_("Garov summasi"), max_digits=12, decimal_places=2)
    deposit_returned    = models.BooleanField(_("Garov qaytarildi"), default=False)
    deposit_returned_at = models.DateTimeField(_("Garov qaytarilgan sana"), null=True, blank=True)

    extended_days = models.PositiveIntegerField(_("Uzaytirilgan kunlar"), default=0)
    notes         = models.TextField(_("Qo'shimcha eslatmalar"), blank=True)

    class Meta:
        verbose_name        = _("Ijara")
        verbose_name_plural = _("Ijaralar")
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.user.phone} - {self.book_copy.book.title}"

    def save(self, *args, **kwargs):
        if self.status == RentalStatus.ACTIVE and not self.rented_at:
            self.rented_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        from django.utils.timezone import now
        return (
            self.status == RentalStatus.ACTIVE and
            self.due_date < now().date()
        )


class RentalExtension(TimeStampedModel):
    """Ijara muddatini uzaytirish tarixi"""

    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        related_name='extensions',
        verbose_name=_("Ijara")
    )
    extended_by_days = models.PositiveIntegerField(_("Uzaytirilgan kunlar"))
    new_due_date     = models.DateField(_("Yangi muddat"))
    reason           = models.TextField(_("Sabab"), blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved_extensions',
        verbose_name=_("Tasdiqlagan admin")
    )

    class Meta:
        verbose_name        = _("Ijara uzaytirish")
        verbose_name_plural = _("Ijara uzaytirishlar")
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.rental} (+{self.extended_by_days} kun)"
