from django.db import models
from apps.common.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
import uuid


class Genre(TimeStampedModel):
    name = models.CharField(_("Janr"), max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(_("Tavsif"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Janr")
        verbose_name_plural = _("Janrlar")



class Author(TimeStampedModel):
    name = models.CharField(_("Muallif"), max_length=200)
    bio = models.TextField(_("Biografiya"), blank=True)
    birth_date = models.DateField(_("Tug‘ilgan sana"), null=True, blank=True)
    photo = models.ImageField(_("Rasm"), upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Muallif")
        verbose_name_plural = _("Mualliflar")



class Publisher(TimeStampedModel):
    name = models.CharField(_("Nashriyot"), max_length=200)
    country = models.CharField(_("Mamlakat"), max_length=100, blank=True)
    website = models.URLField(_("Veb-sayt"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Nashriyot")
        verbose_name_plural = _("Nashriyotlar")


class Book(TimeStampedModel):
    title = models.CharField(_("Kitob nomi"), max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(_("Tavsif"), blank=True)
    isbn = models.CharField(_("ISBN"), max_length=20, unique=True)
    published_date = models.DateField(_("Nashr etilgan sana"), null=True, blank=True)
    price = models.DecimalField(_("Narxi"), max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(_("Zaxiradagi soni"), default=0)
    cover_image = models.ImageField(_("Muqova"), upload_to='books/', blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Kitob")
        verbose_name_plural = _("Kitoblar")
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def authors(self):
        return [self.author] if self.author else []

    @property
    def total_copies(self):
        return self.copies.count()

    @property
    def available_copies(self):
        return self.copies.exclude(status__in=['lost', 'poor']).exclude(rentals__status='active').count()

    @property
    def genres(self):
        return [self.genre] if self.genre else []

    @property
    def language(self):
        return 'uz'

    @property
    def page_count(self):
        return 250

    @property
    def published_year(self):
        return self.published_date.year if self.published_date else 2024

    @property
    def rental_price_daily(self):
        from decimal import Decimal
        return (self.price * Decimal('0.01')).quantize(Decimal('0.01'))

    @property
    def rental_price_weekly(self):
        from decimal import Decimal
        return (self.price * Decimal('0.05')).quantize(Decimal('0.01'))

    @property
    def rental_price_monthly(self):
        from decimal import Decimal
        return (self.price * Decimal('0.15')).quantize(Decimal('0.01'))

    @property
    def deposit_amount(self):
        return self.price

    @property
    def is_active(self):
        return True

    @property
    def preview_pages(self):
        return ""


class BookCopy(TimeStampedModel):
    """
    Har bir nusxa alohida (Inventory)
    """

    class Status(models.TextChoices):
        NEW  = 'new',  _('Yangi')
        GOOD = 'good', _('Yaxshi')
        FAIR = 'fair', _("O'rtacha")      # escaped apostrophe
        POOR = 'poor', _('Eskirgan')
        LOST = 'lost', _("Yo'qolgan")     # escaped apostrophe

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='copies',
        verbose_name=_("Kitob"),
    )
    copy_code = models.CharField(
        _("Nusxa kodi"),
        max_length=50,
        unique=True,        # e.g. BK-001-01
    )
    status = models.CharField(
        _("Holati"),
        max_length=20,
        choices=Status.choices,
        default=Status.GOOD,
        db_index=True,
    )
    location = models.CharField(
        _("Joylashuvi"),
        max_length=100,
        blank=True,         # filial yoki ombor
    )
    notes = models.TextField(_("Izoh"), blank=True)

    class Meta:
        verbose_name = _("Kitob nusxasi")
        verbose_name_plural = _("Kitob nusxalari")
        ordering = ['copy_code']

    def __str__(self) -> str:
        return f"{self.book.title} - {self.copy_code}"

    @property
    def is_available(self) -> bool:
        """Nusxa ijarada emasligi va yo'qolmaganligini tekshiradi."""
        return (
            self.status not in (self.Status.LOST, self.Status.POOR)
            and not self.rentals.filter(status='active').exists()
        )
    