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
from .views import UserViewSet, LoginView, LogoutView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    # Auth
    path('login/',          LoginView.as_view(),        name='login'),
    path('logout/',         LogoutView.as_view(),        name='logout'),
    path('token/refresh/',  TokenRefreshView.as_view(),  name='token-refresh'),
]

# Barcha endpointlar:
# POST /api/v1/users/login/              — telefon + parol → token
# POST /api/v1/users/logout/             — refresh token blacklist
# POST /api/v1/users/token/refresh/      — access token yangilash
# POST /api/v1/users/register/           — ro'yxatdan o'tish
# POST /api/v1/users/verify_phone/       — SMS tasdiqlash
# GET  /api/v1/users/me/                 — o'z profili
# PATCH /api/v1/users/update_me/         — profilni yangilash