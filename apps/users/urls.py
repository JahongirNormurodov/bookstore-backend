# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]

# Yaratilgan endpointlar:
# GET    /api/v1/users/          — list (admin)
# POST   /api/v1/users/register/ — ro'yxatdan o'tish
# GET    /api/v1/users/me/       — o'z profili
# PATCH  /api/v1/users/me/update/
# POST   /api/v1/users/verify_phone/


# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, 
    LoginView, 
    LogoutView,
    WishlistViewSet,
    LoyaltyPointsViewSet,
    TrustScoreViewSet,
    SearchHistoryViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'loyalty-points', LoyaltyPointsViewSet, basename='loyalty-points')
router.register(r'trust-scores', TrustScoreViewSet, basename='trust-scores')
router.register(r'search-history', SearchHistoryViewSet, basename='search-history')

urlpatterns = [
    path('', include(router.urls)),

    # Auth
    path('login/',          LoginView.as_view(),        name='login'),
    path('logout/',         LogoutView.as_view(),        name='logout'),
    path('token/refresh/',  TokenRefreshView.as_view(),  name='token-refresh'),
]

# Barcha endpointlar:
# POST /api/v1/users/login/                    — telefon + parol → token
# POST /api/v1/users/logout/                   — refresh token blacklist
# POST /api/v1/users/token/refresh/            — access token yangilash
# POST /api/v1/users/users/register/           — ro'yxatdan o'tish
# POST /api/v1/users/users/send-code/          — SMS yuborish
# POST /api/v1/users/users/verify-code/        — SMS tasdiqlash
# GET  /api/v1/users/users/me/                 — o'z profili
# PATCH /api/v1/users/users/update-me/         — profilni yangilash
# GET  /api/v1/users/wishlist/                 — wishlist ro'yxati
# POST /api/v1/users/wishlist/                 — wishlistga qo'shish
# DELETE /api/v1/users/wishlist/{id}/          — wishlistdan o'chirish
# DELETE /api/v1/users/wishlist/clear/         — barchasini o'chirish
# GET  /api/v1/users/loyalty-points/           — ball tarixi
# GET  /api/v1/users/loyalty-points/balance/   — joriy balans
# GET  /api/v1/users/trust-scores/             — trust score tarixi
# GET  /api/v1/users/trust-scores/current/     — joriy trust score
# GET  /api/v1/users/search-history/           — qidiruv tarixi
# DELETE /api/v1/users/search-history/clear/   — tarixni tozalash