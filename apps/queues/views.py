# queues/views.py
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import BookQueue, BookNotification
from .serializers import (
    BookQueueSerializer, 
    BookQueueCreateSerializer,
    BookNotificationSerializer,
    BookNotificationCreateSerializer
)


class BookQueueViewSet(viewsets.ModelViewSet):
    """Book queue management"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'book']
    ordering_fields = ['created_at', 'position']
    ordering = ['position']
    
    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False) or not user.is_authenticated:
            return BookQueue.objects.none()
        if user.is_staff:
            return BookQueue.objects.select_related('user', 'book').all()
        return BookQueue.objects.filter(user=user).select_related('book')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookQueueCreateSerializer
        return BookQueueSerializer
    
    @action(detail=False, methods=['get'])
    def my_queue(self, request):
        """Get current user's queue entries"""
        queues = self.get_queryset().filter(user=request.user, status='waiting')
        serializer = self.get_serializer(queues, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel queue entry"""
        queue_entry = self.get_object()
        if queue_entry.user != request.user and not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
        
        queue_entry.status = 'cancelled'
        queue_entry.save()
        
        # Reorder positions
        BookQueue.objects.filter(
            book=queue_entry.book,
            status='waiting',
            position__gt=queue_entry.position
        ).update(position=models.F('position') - 1)
        
        return Response({'status': 'Queue entry cancelled'})


class BookNotificationViewSet(viewsets.ModelViewSet):
    """Book notification subscriptions"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_notified', 'book']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False) or not user.is_authenticated:
            return BookNotification.objects.none()
        if user.is_staff:
            return BookNotification.objects.select_related('user', 'book').all()
        return BookNotification.objects.filter(user=user).select_related('book')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookNotificationCreateSerializer
        return BookNotificationSerializer
    
    @action(detail=False, methods=['get'])
    def my_notifications(self, request):
        """Get current user's notification subscriptions"""
        notifications = self.get_queryset().filter(user=request.user, is_notified=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def unsubscribe(self, request, pk=None):
        """Unsubscribe from book notifications"""
        notification = self.get_object()
        if notification.user != request.user and not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
        
        notification.delete()
        return Response({'status': 'Unsubscribed successfully'}, status=status.HTTP_204_NO_CONTENT)
