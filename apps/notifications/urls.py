# notifications/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]

# Yaratilgan endpointlar:
# GET  /api/v1/notifications/                   — bildirishnomalar
# POST /api/v1/notifications/{id}/mark_as_read/
# POST /api/v1/notifications/mark_all_read/