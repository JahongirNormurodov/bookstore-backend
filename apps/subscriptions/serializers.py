from rest_framework import serializers
from .models import Subscription, SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id',
            'name',
            'slug',
            'price_monthly',
            'max_books_per_month',
            'max_simultaneous_books',
            'is_unlimited',
            'description',
            'is_active',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'user_phone',
            'plan',
            'plan_name',
            'status',
            'start_date',
            'end_date',
            'cancelled_at',
            'auto_renew',
            'notes',
        ]
        read_only_fields = ['status', 'cancelled_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        validated_data['status'] = 'active'

        # Cancel current active subscription if any
        active_sub = Subscription.objects.filter(user=request.user, status='active').first()
        if active_sub:
            active_sub.status = 'cancelled'
            active_sub.save(update_fields=['status'])

        return super().create(validated_data)
