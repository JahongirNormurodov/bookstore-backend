# payments/serializers.py
from rest_framework import serializers
from decimal import Decimal
from django.db.models import Sum
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
        read_only_fields = ['id', 'user', 'amount', 'status', 'created_at', 'updated_at']
    
    def get_rental_details(self, obj):
        if obj.rental:
            return {
                'id': str(obj.rental.id),
                'book': obj.rental.book_copy.book.title,
                'due_date': obj.rental.due_date
            }
        return None


class PaymentCreateSerializer(serializers.ModelSerializer):
    """To'lov yaratish — user, amount va status serverda aniqlanadi (mijoz yubora olmaydi)."""

    class Meta:
        model = Payment
        fields = [
            'payment_type', 'payment_method',
            'rental', 'subscription', 'description'
        ]

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        payment_type = attrs.get('payment_type')
        rental = attrs.get('rental')
        subscription = attrs.get('subscription')

        # Bog'liq obyektlar so'rovchiga tegishli ekanini tekshirish (IDOR oldini olish)
        if rental and rental.user_id != user.id:
            raise serializers.ValidationError("Bu ijara sizga tegishli emas.")
        if subscription and subscription.user_id != user.id:
            raise serializers.ValidationError("Bu obuna sizga tegishli emas.")

        # Summani turga qarab serverda hisoblash
        if payment_type == Payment.PaymentType.RENTAL:
            if not rental:
                raise serializers.ValidationError("Ijara to'lovi uchun rental majburiy.")
            attrs['_amount'] = rental.rental_price
        elif payment_type == Payment.PaymentType.DEPOSIT:
            if not rental:
                raise serializers.ValidationError("Garov uchun rental majburiy.")
            attrs['_amount'] = rental.deposit_amount
        elif payment_type == Payment.PaymentType.PENALTY:
            if not rental:
                raise serializers.ValidationError("Jarima to'lovi uchun rental majburiy.")
            unpaid = rental.penalties.filter(is_paid=False).aggregate(
                total=Sum('penalty_amount')
            )['total'] or Decimal('0')
            if unpaid <= 0:
                raise serializers.ValidationError("To'lanmagan jarima yo'q.")
            attrs['_amount'] = unpaid
        elif payment_type == Payment.PaymentType.SUBSCRIPTION:
            if not subscription:
                raise serializers.ValidationError("Obuna to'lovi uchun subscription majburiy.")
            attrs['_amount'] = subscription.plan.price_monthly
        else:
            raise serializers.ValidationError("Bu turdagi to'lovni mijoz yarata olmaydi.")

        return attrs

    def create(self, validated_data):
        amount = validated_data.pop('_amount')
        request = self.context['request']
        # status PENDING bo'lib qoladi — haqiqiy to'lov gateway tomonidan
        # tasdiqlanmaguncha COMPLETED bo'lmaydi.
        return Payment.objects.create(
            user=request.user,
            amount=amount,
            status=Payment.PaymentStatus.PENDING,
            **validated_data
        )


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
