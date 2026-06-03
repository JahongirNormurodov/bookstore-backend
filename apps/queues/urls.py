# queues/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookQueueViewSet, BookNotificationViewSet

router = DefaultRouter()
router.register('queues', BookQueueViewSet, basename='queue')
router.register('notifications', BookNotificationViewSet, basename='book-notification')

urlpatterns = [
    path('', include(router.urls)),
]
