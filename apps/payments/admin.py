# payments/admin.py
from django.contrib import admin
from .models import Payment, Penalty


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_type', 'payment_method', 'status', 'created_at']
    list_filter = ['payment_type', 'payment_method', 'status', 'created_at']
    search_fields = ['user__phone', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy', {
            'fields': ('user', 'amount', 'payment_type', 'payment_method', 'status')
        }),
        ('Bog\'liq obyektlar', {
            'fields': ('rental', 'subscription')
        }),
        ('Tafsilotlar', {
            'fields': ('transaction_id', 'description', 'notes')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ['rental', 'days_overdue', 'penalty_amount', 'is_paid', 'paid_at', 'created_at']
    list_filter = ['is_paid', 'created_at']
    search_fields = ['rental__user__phone', 'rental__book_copy__book__title']
    readonly_fields = ['created_at', 'updated_at']
