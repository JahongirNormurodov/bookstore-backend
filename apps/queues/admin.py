# queues/admin.py
from django.contrib import admin
from .models import BookQueue, BookNotification


@admin.register(BookQueue)
class BookQueueAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'status', 'position', 'created_at', 'notified_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__phone', 'book__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['book', 'created_at']


@admin.register(BookNotification)
class BookNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'is_notified', 'notified_at', 'created_at']
    list_filter = ['is_notified', 'created_at']
    search_fields = ['user__phone', 'book__title']
    readonly_fields = ['created_at', 'updated_at']
