# payments/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.utils import timezone
from .models import Payment, Penalty
from .serializers import PaymentSerializer, PaymentCreateSerializer, PenaltySerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """To'lovlarni boshqarish.

    Mijoz faqat o'zi uchun to'lov yarata oladi; user/amount/status serverda
    aniqlanadi. To'lovni o'zgartirish/o'chirish faqat adminlarga ruxsat etilgan.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_type', 'payment_method', 'status']
    search_fields = ['transaction_id', 'user__phone']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False) or not user.is_authenticated:
            return Payment.objects.none()
        if user.is_staff:
            return Payment.objects.select_related('user', 'rental', 'subscription').all()
        return Payment.objects.filter(user=user).select_related('rental', 'subscription')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PaymentCreateSerializer
        return PaymentSerializer

    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        payments = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(payments)
        serializer = PaymentSerializer(page or payments, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        stats = Payment.objects.aggregate(
            total_amount=models.Sum('amount'),
            total_count=models.Count('id'),
            completed_count=models.Count('id', filter=models.Q(status='completed')),
        )
        return Response(stats)


class PenaltyViewSet(viewsets.ReadOnlyModelViewSet):
    """Jarimalar. Mijoz faqat o'z jarimalarini ko'ra oladi.

    Jarima yaratish/o'zgartirish/to'langan deb belgilash faqat adminlarda —
    aks holda mijoz o'z jarimasini bepul yopib qo'yishi mumkin edi.
    """
    serializer_class = PenaltySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_paid']
    ordering_fields = ['created_at', 'penalty_amount', 'days_overdue']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action == 'mark_paid':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False) or not user.is_authenticated:
            return Penalty.objects.none()
        if user.is_staff:
            return Penalty.objects.select_related('rental__user', 'rental__book_copy__book').all()
        return Penalty.objects.filter(
            rental__user=user
        ).select_related('rental__book_copy__book')

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Jarimani to'langan deb belgilash (faqat admin)."""
        penalty = self.get_object()
        penalty.is_paid = True
        penalty.paid_at = timezone.now()
        penalty.save(update_fields=['is_paid', 'paid_at'])
        return Response({'status': 'Jarima to\'langan deb belgilandi'})
