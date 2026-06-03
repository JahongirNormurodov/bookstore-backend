# couriers/admin.py
from django.contrib import admin
from .models import Courier, Delivery


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'vehicle_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'vehicle_type']
    search_fields = ['user__phone', 'phone', 'vehicle_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['rental', 'courier', 'delivery_type', 'status', 'scheduled_date', 'completed_at']
    list_filter = ['delivery_type', 'status', 'scheduled_date']
    search_fields = ['rental__user__phone', 'courier__user__phone', 'address']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy', {
            'fields': ('rental', 'courier', 'delivery_type', 'status')
        }),
        ('Manzil va vaqt', {
            'fields': ('address', 'scheduled_date', 'scheduled_time', 'completed_at')
        }),
        ('Qo\'shimcha', {
            'fields': ('notes', 'signature', 'photo')
        }),
        ('Tizim', {
            'fields': ('created_at', 'updated_at')
        }),
    )
