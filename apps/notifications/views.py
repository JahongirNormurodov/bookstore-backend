from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False) or not user.is_authenticated:
            return Notification.objects.none()
        if user.is_staff:
            return Notification.objects.all().select_related(
                'user', 'related_rental', 'related_book'
            )
        return Notification.objects.filter(user=user).select_related(
            'user', 'related_rental', 'related_book'
        )

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response(
            {"message": "Bildirishnoma o'qildi deb belgilandi."}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True, read_at=timezone.now())
        return Response(
            {"message": "Barcha bildirishnomalar o'qildi deb belgilandi."}, status=status.HTTP_200_OK
        )
