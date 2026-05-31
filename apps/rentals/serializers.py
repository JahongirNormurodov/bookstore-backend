# rentals/serializers.py
from rest_framework import serializers
from django.utils.timezone import now
from .models import Rental, RentalExtension
from apps.books.serializers import BookListSerializer


class RentalSerializer(serializers.ModelSerializer):
    """Ijarani ko'rish uchun"""
    book             = BookListSerializer(source='book_copy.book', read_only=True)
    book_copy        = serializers.StringRelatedField(read_only=True)
    user_phone       = serializers.CharField(source='user.phone', read_only=True)
    is_overdue       = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Rental
        fields = [
            'id', 'user_phone', 'book', 'book_copy', 'status',
            'rented_at', 'due_date', 'returned_at',
            'rental_price', 'deposit_amount',
            'deposit_returned', 'deposit_returned_at',
            'extended_days', 'is_overdue', 'notes'
        ]
        read_only_fields = [
            'rented_at', 'returned_at',
            'extended_days', 'is_overdue',
            'deposit_returned_at'
        ]


class RentalCreateSerializer(serializers.ModelSerializer):
    """Yangi ijara yaratish uchun"""

    class Meta:
        model  = Rental
        fields = ['book_copy', 'due_date', 'notes']

    def validate_due_date(self, value):
        if value <= now().date():
            raise serializers.ValidationError(
                "Qaytarish muddati bugundan keyin bo'lishi kerak."
            )
        return value

    def validate_book_copy(self, value):
        if not value.is_available:
            raise serializers.ValidationError(
                "Bu kitob nusxasi hozir mavjud emas."
            )
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            active_rentals = Rental.objects.filter(
                user=request.user,
                status__in=['pending', 'active']
            )
            # Foydalanuvchining obunasidagi limitni tekshirish
            plan = getattr(request.user, 'active_plan', None)
            if plan and not plan.is_unlimited:
                if active_rentals.count() >= plan.max_simultaneous_books:
                    raise serializers.ValidationError(
                        "Siz bir vaqtda ruxsat etilgan miqdordagi kitobni oldingiz."
                    )
        return attrs


class RentalExtensionSerializer(serializers.ModelSerializer):
    """Ijara muddatini uzaytirish"""

    class Meta:
        model  = RentalExtension
        fields = ['id', 'rental', 'extended_by_days', 'new_due_date', 'reason']
        read_only_fields = ['id']

    def validate_new_due_date(self, value):
        if value <= now().date():
            raise serializers.ValidationError(
                "Yangi muddat bugundan keyin bo'lishi kerak."
            )
        return value

    def validate(self, attrs):
        rental = attrs.get('rental')
        if rental and rental.status not in ['active', 'overdue']:
            raise serializers.ValidationError(
                "Faqat faol yoki muddati o'tgan ijarani uzaytirish mumkin."
            )
        return attrs