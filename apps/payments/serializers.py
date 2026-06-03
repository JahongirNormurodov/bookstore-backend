# payments/serializers.py
from rest_framework import serializers
from .models import Payment, Penalty


class PaymentSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    rental_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_phone', 'amount', 'payment_type', 
            'payment_method', 'status', 'rental', 'rental_details',
            'subscription', 'transaction_id', 'description', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_rental_details(self, obj):
        if obj.rental:
            return {
                'id': str(obj.rental.id),
                'book': obj.rental.book_copy.book.title,
                'due_date': obj.rental.due_date
            }
        return None


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'user', 'amount', 'payment_type', 'payment_method', 
            'rental', 'subscription', 'description', 'notes'
        ]


class PenaltySerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source='rental.user.phone', read_only=True)
    book_title = serializers.CharField(source='rental.book_copy.book.title', read_only=True)
    
    class Meta:
        model = Penalty
        fields = [
            'id', 'rental', 'user_phone', 'book_title',
            'days_overdue', 'penalty_amount', 'is_paid', 
            'paid_at', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
