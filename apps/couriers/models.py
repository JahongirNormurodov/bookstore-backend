# couriers/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel
from apps.users.models import User


class Courier(TimeStampedModel):
    """Kuryer profili"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='courier_profile',
        verbose_name=_("Foydalanuvchi")
    )
    phone = models.CharField(_("Telefon"), max_length=15)
    vehicle_type = models.CharField(_("Transport turi"), max_length=50, blank=True)
    vehicle_number = models.CharField(_("Transport raqami"), max_length=20, blank=True)
    is_active = models.BooleanField(_("Faol"), default=True)
    
    class Meta:
        verbose_name = _("Kuryer")
        verbose_name_plural = _("Kuryerlar")
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"


class Delivery(TimeStampedModel):
    """Yetkazib berish"""
    
    class DeliveryType(models.TextChoices):
        PICKUP = 'pickup', _("Olib borish")
        RETURN = 'return', _("Olib kelish")
    
    class Status(models.TextChoices):
        PENDING = 'pending', _("Kutilmoqda")
        ASSIGNED = 'assigned', _("Tayinlangan")
        IN_TRANSIT = 'in_transit', _("Yo'lda")
        DELIVERED = 'delivered', _("Yetkazildi")
        CANCELLED = 'cancelled', _("Bekor qilingan")
    
    rental = models.ForeignKey(
        'rentals.Rental',
        on_delete=models.CASCADE,
        related_name='deliveries',
        verbose_name=_("Ijara")
    )
    courier = models.ForeignKey(
        Courier,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='deliveries',
        verbose_name=_("Kuryer")
    )
    delivery_type = models.CharField(_("Turi"), max_length=20, choices=DeliveryType.choices)
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    
    address = models.TextField(_("Manzil"))
    scheduled_date = models.DateField(_("Rejalashtirilgan sana"))
    scheduled_time = models.TimeField(_("Rejalashtirilgan vaqt"), null=True, blank=True)
    
    completed_at = models.DateTimeField(_("Bajarilgan vaqt"), null=True, blank=True)
    notes = models.TextField(_("Izohlar"), blank=True)
    signature = models.ImageField(_("Mijoz imzosi"), upload_to='signatures/', blank=True, null=True)
    photo = models.ImageField(_("Kitob holati rasmi"), upload_to='delivery_photos/', blank=True, null=True)
    
    class Meta:
        verbose_name = _("Yetkazib berish")
        verbose_name_plural = _("Yetkazib berishlar")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_delivery_type_display()} - {self.rental.user.phone}"
