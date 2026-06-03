# admin_panel/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel
from apps.users.models import User


class StaffRole(models.Model):
    """Xodimlar rollari"""
    
    name = models.CharField(_("Rol nomi"), max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(_("Tavsif"), blank=True)
    
    # Permissions
    can_manage_books = models.BooleanField(_("Kitoblarni boshqarish"), default=False)
    can_manage_rentals = models.BooleanField(_("Ijaralarni boshqarish"), default=False)
    can_manage_users = models.BooleanField(_("Foydalanuvchilarni boshqarish"), default=False)
    can_manage_subscriptions = models.BooleanField(_("Obunalarni boshqarish"), default=False)
    can_view_reports = models.BooleanField(_("Hisobotlarni ko'rish"), default=False)
    can_manage_settings = models.BooleanField(_("Sozlamalarni boshqarish"), default=False)
    can_manage_couriers = models.BooleanField(_("Kuryerlarni boshqarish"), default=False)
    
    class Meta:
        verbose_name = _("Xodim roli")
        verbose_name_plural = _("Xodim rollari")
    
    def __str__(self):
        return self.name


class StaffMember(TimeStampedModel):
    """Xodimlar"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        verbose_name=_("Foydalanuvchi")
    )
    role = models.ForeignKey(
        StaffRole,
        on_delete=models.PROTECT,
        related_name='staff_members',
        verbose_name=_("Rol")
    )
    employee_id = models.CharField(_("Xodim ID"), max_length=50, unique=True)
    is_active = models.BooleanField(_("Faol"), default=True)
    notes = models.TextField(_("Izohlar"), blank=True)
    
    class Meta:
        verbose_name = _("Xodim")
        verbose_name_plural = _("Xodimlar")
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role.name})"


class ActivityLog(TimeStampedModel):
    """Faoliyat loglari"""
    
    class ActionType(models.TextChoices):
        CREATE = 'create', _("Yaratildi")
        UPDATE = 'update', _("Yangilandi")
        DELETE = 'delete', _("O'chirildi")
        LOGIN = 'login', _("Kirdi")
        LOGOUT = 'logout', _("Chiqdi")
        APPROVE = 'approve', _("Tasdiqlandi")
        REJECT = 'reject', _("Rad etildi")
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs',
        verbose_name=_("Foydalanuvchi")
    )
    action = models.CharField(_("Harakat"), max_length=20, choices=ActionType.choices)
    model_name = models.CharField(_("Model nomi"), max_length=100)
    object_id = models.CharField(_("Obyekt ID"), max_length=100, blank=True)
    description = models.TextField(_("Tavsif"))
    ip_address = models.GenericIPAddressField(_("IP manzil"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Faoliyat logi")
        verbose_name_plural = _("Faoliyat loglari")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['model_name', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.model_name}"


class BlogPost(TimeStampedModel):
    """Blog postlari"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _("Qoralama")
        PUBLISHED = 'published', _("Nashr qilingan")
        ARCHIVED = 'archived', _("Arxivlangan")
    
    title = models.CharField(_("Sarlavha"), max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(_("Matn"))
    excerpt = models.TextField(_("Qisqacha"), blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts',
        verbose_name=_("Muallif")
    )
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.DRAFT)
    featured_image = models.ImageField(_("Asosiy rasm"), upload_to='blog/', blank=True, null=True)
    published_at = models.DateTimeField(_("Nashr sanasi"), null=True, blank=True)
    views_count = models.PositiveIntegerField(_("Ko'rishlar soni"), default=0)
    
    class Meta:
        verbose_name = _("Blog posti")
        verbose_name_plural = _("Blog postlari")
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title


class FAQ(TimeStampedModel):
    """Ko'p so'raladigan savollar"""
    
    question = models.CharField(_("Savol"), max_length=500)
    answer = models.TextField(_("Javob"))
    order = models.PositiveIntegerField(_("Tartib"), default=0)
    is_active = models.BooleanField(_("Faol"), default=True)
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQlar")
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.question[:100]
