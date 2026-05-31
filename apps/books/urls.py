# books/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]

# Yaratilgan endpointlar:
# GET /api/v1/books/          — kitoblar ro'yxati
# GET /api/v1/books/{id}/     — bitta kitob


# books/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookCopyViewSet

router = DefaultRouter()
router.register(r'',       BookViewSet,     basename='book')
router.register(r'copies', BookCopyViewSet, basename='book-copy')

urlpatterns = [
    path('', include(router.urls)),
]

# Endpointlar:
# GET    /api/v1/books/               — kitoblar ro'yxati
# GET    /api/v1/books/{id}/          — bitta kitob
# GET    /api/v1/books/copies/        — barcha nusxalar
# GET    /api/v1/books/copies/{id}/   — bitta nusxa
# POST   /api/v1/books/copies/        — nusxa qo'shish (admin)
# PATCH  /api/v1/books/copies/{id}/   — tahrirlash (admin)
# DELETE /api/v1/books/copies/{id}/   — o'chirish (admin)

# books/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookCopyViewSet

router = DefaultRouter()
router.register(r'',       BookViewSet,     basename='book')
router.register(r'copies', BookCopyViewSet, basename='book-copy')

urlpatterns = [
    path('', include(router.urls)),
]

# Endpointlar:
# GET  /api/v1/books/            — kitoblar
# GET  /api/v1/books/{id}/       — bitta kitob
# GET  /api/v1/books/copies/     — nusxalar (admin)
# POST /api/v1/books/copies/     — nusxa qo'shish (admin)