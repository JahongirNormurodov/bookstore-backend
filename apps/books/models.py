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
    
    # Additional images for book details
    image_2 = models.ImageField(_("Rasm 2"), upload_to='books/', blank=True, null=True)
    image_3 = models.ImageField(_("Rasm 3"), upload_to='books/', blank=True, null=True)
    image_4 = models.ImageField(_("Rasm 4"), upload_to='books/', blank=True, null=True)
    
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    
    # Book details
    language = models.CharField(_("Til"), max_length=50, default='uz')
    page_count = models.PositiveIntegerField(_("Sahifalar soni"), default=0)
    rating = models.DecimalField(_("Reyting"), max_digits=3, decimal_places=2, default=0.0)
    reviews_count = models.PositiveIntegerField(_("Sharhlar soni"), default=0)
    
    # Preview
    preview_pages = models.TextField(_("Preview sahifalar"), blank=True, help_text=_("Bir necha sahifa matni"))
    
    # Rental settings
    is_active = models.BooleanField(_("Faol"), default=True)
    max_rental_days = models.PositiveIntegerField(_("Maksimal ijara muddati (kun)"), default=60)

    class Meta:
        verbose_name = _("Kitob")
        verbose_name_plural = _("Kitoblar")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['isbn']),
            models.Index(fields=['is_active', 'rating']),
        ]

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
        return self.copies.exclude(
            status__in=['lost', 'poor']
        ).exclude(
            rentals__status__in=['pending', 'active', 'overdue']
        ).count()

    @property
    def genres(self):
        return [self.genre] if self.genre else []

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

    def calculate_rental_price(self, days):
        """Ijara kunlari soniga qarab narxni hisoblaydi (oylik/haftalik/kunlik tariflar bo'yicha)."""
        from decimal import Decimal
        days = int(days)
        if days <= 0:
            raise ValueError("Ijara muddati kamida 1 kun bo'lishi kerak.")

        months, remainder = divmod(days, 30)
        weeks, rem_days = divmod(remainder, 7)

        total = (
            self.rental_price_monthly * months
            + self.rental_price_weekly * weeks
            + self.rental_price_daily * rem_days
        )
        return total.quantize(Decimal('0.01'))
    
    @property
    def next_available_date(self):
        """Keyingi nusxa qachon bo'shashi"""
        from django.utils import timezone
        active_rentals = self.copies.filter(rentals__status='active').values_list('rentals__due_date', flat=True)
        if active_rentals:
            return min(active_rentals)
        return timezone.now().date()
    
    @property
    def queue_count(self):
        """Navbatdagi odamlar soni"""
        return self.queues.filter(status='waiting').count()
    
    def update_rating(self):
        """Kitob reytingini yangilash"""
        from django.db.models import Avg, Count
        stats = self.reviews.filter(is_approved=True).aggregate(
            avg_rating=Avg('rating'),
            count=Count('id')
        )
        self.rating = stats['avg_rating'] or 0.0
        self.reviews_count = stats['count'] or 0
        self.save(update_fields=['rating', 'reviews_count'])


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
    barcode = models.CharField(_("Barcode/QR kod"), max_length=100, blank=True, unique=True)
    rental_count = models.PositiveIntegerField(_("Necha marta ijaraga berilgan"), default=0)

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
            and not self.rentals.filter(
                status__in=['pending', 'active', 'overdue']
            ).exists()
        )


class BookReview(TimeStampedModel):
    """Kitob sharhlari va reytinglari"""
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_("Kitob")
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='book_reviews',
        verbose_name=_("Foydalanuvchi")
    )
    rating = models.PositiveSmallIntegerField(_("Reyting"), help_text=_("1-5"))
    review_text = models.TextField(_("Sharh"), blank=True)
    is_approved = models.BooleanField(_("Tasdiqlangan"), default=False)
    
    class Meta:
        verbose_name = _("Kitob sharhi")
        verbose_name_plural = _("Kitob sharhlari")
        ordering = ['-created_at']
        unique_together = ['book', 'user']
    
    def __str__(self):
        return f"{self.user.phone} - {self.book.title} ({self.rating}/5)"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update book rating
        self.book.update_rating()


class SimilarBook(TimeStampedModel):
    """O'xshash kitoblar"""
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='similar_books',
        verbose_name=_("Kitob")
    )
    similar_to = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='similar_from',
        verbose_name=_("O'xshash kitob")
    )
    similarity_score = models.DecimalField(_("O'xshashlik darajasi"), max_digits=3, decimal_places=2, default=0.0)
    
    class Meta:
        verbose_name = _("O'xshash kitob")
        verbose_name_plural = _("O'xshash kitoblar")
        unique_together = ['book', 'similar_to']
    
    def __str__(self):
        return f"{self.book.title} ~ {self.similar_to.title}"
    