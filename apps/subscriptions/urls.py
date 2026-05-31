# subscriptions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, SubscriptionPlanViewSet

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='subscription-plan')
router.register(r'',      SubscriptionViewSet,     basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
]

# Yaratilgan endpointlar:
# GET  /api/v1/subscriptions/           — obunalar
# POST /api/v1/subscriptions/           — obuna olish
# POST /api/v1/subscriptions/{id}/cancel/
# GET  /api/v1/subscriptions/plans/     — tariflar ro'yxati