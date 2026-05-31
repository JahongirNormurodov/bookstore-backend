# rentals/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentalViewSet

router = DefaultRouter()
router.register(r'', RentalViewSet, basename='rental')

urlpatterns = [
    path('', include(router.urls)),
]

# Yaratilgan endpointlar:
# GET    /api/v1/rentals/              — ijaralar ro'yxati
# POST   /api/v1/rentals/              — yangi ijara
# GET    /api/v1/rentals/{id}/         — bitta ijara
# POST   /api/v1/rentals/{id}/return_book/
# POST   /api/v1/rentals/{id}/extend/