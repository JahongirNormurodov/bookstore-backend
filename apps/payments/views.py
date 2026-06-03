# payments/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Payment, Penalty
from .serializers import PaymentSerializer, PaymentCreateSerializer, PenaltySerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Payment management"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_type', 'payment_method', 'status', 'user']
    search_fields = ['transaction_id', 'user__phone']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.select_related('user', 'rental', 'subscription').all()
        return Payment.objects.filter(user=user).select_related('rental', 'subscription')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PaymentCreateSerializer
        return PaymentSerializer
    
    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        """Get current user's payments"""
        payments = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Payment statistics (admin only)"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
        
        from django.db.models import Sum, Count
        stats = Payment.objects.aggregate(
            total_amount=Sum('amount'),
            total_count=Count('id'),
            completed_count=Count('id', filter=models.Q(status='completed'))
        )
        return Response(stats)


class PenaltyViewSet(viewsets.ModelViewSet):
    """Penalty management"""
    permission_classes = [IsAuthenticated]
    serializer_class = PenaltySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_paid', 'rental__user']
    ordering_fields = ['created_at', 'penalty_amount', 'days_overdue']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Penalty.objects.select_related('rental__user', 'rental__book_copy__book').all()
        return Penalty.objects.filter(rental__user=user).select_related('rental__book_copy__book')
    
    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark penalty as paid"""
        penalty = self.get_object()
        from django.utils import timezone
        penalty.is_paid = True
        penalty.paid_at = timezone.now()
        penalty.save()
        return Response({'status': 'Penalty marked as paid'})
