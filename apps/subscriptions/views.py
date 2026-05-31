from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Subscription, SubscriptionPlan
from .serializers import SubscriptionSerializer, SubscriptionPlanSerializer


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Subscription.objects.all().select_related('user', 'plan')
        return Subscription.objects.filter(user=user).select_related('user', 'plan')

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        subscription = self.get_object()
        if subscription.status == 'active':
            subscription.cancel()
            return Response(
                {"message": "Obuna muvaffaqiyatli bekor qilindi."}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Faqat faol obunani bekor qilish mumkin."},
            status=status.HTTP_400_BAD_REQUEST,
        )
