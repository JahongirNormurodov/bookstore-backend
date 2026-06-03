# payments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PenaltyViewSet

router = DefaultRouter()
router.register('payments', PaymentViewSet, basename='payment')
router.register('penalties', PenaltyViewSet, basename='penalty')

urlpatterns = [
    path('', include(router.urls)),
]
