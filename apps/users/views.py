# users/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admin — hammani ko'radi, oddiy user — faqat o'zini
        if user.is_staff:
            return User.objects.all().select_related('profile')
        return User.objects.filter(pk=user.pk).select_related('profile')

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegistrationSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        if self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    # POST /users/register/
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
                    "user_id": str(user.id),
                    "phone": user.phone,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET /users/me/
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# users/views.py
from rest_framework.throttling import ScopedRateThrottle

class UserViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=['post'], throttle_scope='register')
    def register(self, request):
        ...

# auth/views.py — login uchun
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import ScopedRateThrottle

class LoginView(TokenObtainPairView):
    throttle_scope = 'login'   # ← settings dagi 5/minute ishlaydi


# users/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    throttle_scope     = 'login'   # settings da 5/minute


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {"error": "Refresh token kiritilmadi."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()   # token_blacklist ga qo'shadi
            return Response(
                {"message": "Muvaffaqiyatli chiqildi."},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Token yaroqsiz."},
                status=status.HTTP_400_BAD_REQUEST
            )

# users/views.py
from .services import send_verification_sms
from .models import OTPCode

@action(detail=False, methods=['post'], permission_classes=[AllowAny])
def send_otp(self, request):
    serializer = SendOTPSerializer(data=request.data)
    if serializer.is_valid():
        try:
            send_verification_sms(
                phone   = serializer.validated_data['phone'],
                purpose = OTPCode.Purpose.REGISTER
            )
            return Response({"message": "Kod yuborildi."})
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# users/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, OTPCode
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserRegistrationSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
)
from .services import send_verification_sms


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    throttle_scope     = 'login'


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all().select_related('profile')
        return User.objects.filter(pk=user.pk).select_related('profile')

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegistrationSerializer
        if self.action in ['update', 'partial_update', 'update_me']:
            return UserUpdateSerializer
        if self.action == 'send_code':
            return SendOTPSerializer
        if self.action == 'verify_code':
            return VerifyOTPSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'send_code', 'verify_code']:
            return [AllowAny()]
        if self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_throttles(self):
        if self.action == 'register':
            self.throttle_scope = 'register'
        if self.action == 'send_code':
            self.throttle_scope = 'send_otp'
        return super().get_throttles()

    # ───────────────────────────────────────────
    # POST /api/v1/users/register/
    # ───────────────────────────────────────────
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Ro'yxatdan o'tgach darhol SMS yuborish
            try:
                send_verification_sms(
                    phone   = user.phone,
                    purpose = OTPCode.Purpose.REGISTER
                )
            except Exception:
                pass  # SMS kelmasa ham ro'yxat muvaffaqiyatli
            return Response(
                {
                    "message": "Ro'yxatdan o'tdingiz. Telefonga kod yuborildi.",
                    "phone":   user.phone,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ───────────────────────────────────────────
    # POST /api/v1/users/send-code/
    # ───────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='send-code')
    def send_code(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone   = serializer.validated_data['phone']
        purpose = serializer.validated_data.get('purpose', OTPCode.Purpose.REGISTER)

        try:
            send_verification_sms(phone=phone, purpose=purpose)
            return Response(
                {"message": "Tasdiqlash kodi yuborildi."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    # ───────────────────────────────────────────
    # POST /api/v1/users/verify-code/
    # ───────────────────────────────────────────
    @action(detail=False, methods=['post'], url_path='verify-code')
    def verify_code(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user    = serializer.validated_data['user']
        otp     = serializer.validated_data['otp']
        purpose = serializer.validated_data['purpose']

        # Kodni ishlatilgan deb belgilash
        otp.verify()

        # Maqsadga qarab harakat
        if purpose == OTPCode.Purpose.REGISTER:
            profile = user.profile
            profile.is_phone_verified = True
            profile.save(update_fields=['is_phone_verified'])

            # Token qaytarish — login qildirish
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Telefon tasdiqlandi.",
                    "access":  str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK
            )

        if purpose == OTPCode.Purpose.RESET_PASSWORD:
            # Parol tiklash uchun vaqtinchalik token
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message":       "Kod tasdiqlandi. Yangi parol o'rnating.",
                    "reset_token":   str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Kod tasdiqlandi."},
            status=status.HTTP_200_OK
        )

    # ───────────────────────────────────────────
    # GET /api/v1/users/me/
    # ───────────────────────────────────────────
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    # ───────────────────────────────────────────
    # PATCH /api/v1/users/update-me/
    # ───────────────────────────────────────────
    @action(detail=False, methods=['patch'], url_path='update-me')
    def update_me(self, request):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ───────────────────────────────────────────
    # POST /api/v1/users/logout/
    # ───────────────────────────────────────────
    @action(detail=False, methods=['post'])
    def logout(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {"error": "Refresh token kiritilmadi."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Muvaffaqiyatli chiqildi."},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Token yaroqsiz."},
                status=status.HTTP_400_BAD_REQUEST
            )




# Wishlist ViewSet
class WishlistViewSet(viewsets.ModelViewSet):
    """User wishlist management"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('book', 'book__author')
    
    def get_serializer_class(self):
        from .serializers import WishlistSerializer, WishlistCreateSerializer
        if self.action == 'create':
            return WishlistCreateSerializer
        return WishlistSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear all wishlist items"""
        count = self.get_queryset().delete()[0]
        return Response({'message': f'{count} items removed from wishlist'})


# Loyalty Points ViewSet
class LoyaltyPointsViewSet(viewsets.ReadOnlyModelViewSet):
    """User loyalty points history"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        from .models import LoyaltyPoints
        return LoyaltyPoints.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        from .serializers import LoyaltyPointsSerializer
        return LoyaltyPointsSerializer
    
    @action(detail=False, methods=['get'])
    def balance(self, request):
        """Get current loyalty points balance"""
        total = request.user.total_loyalty_points
        return Response({'balance': total})


# Trust Score ViewSet
class TrustScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """User trust score history"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        from .models import TrustScore
        if self.request.user.is_staff:
            return TrustScore.objects.select_related('user', 'changed_by').all()
        return TrustScore.objects.filter(user=self.request.user).select_related('changed_by')
    
    def get_serializer_class(self):
        from .serializers import TrustScoreSerializer
        return TrustScoreSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current trust score"""
        score = request.user.current_trust_score
        return Response({'trust_score': score})


# Search History ViewSet
class SearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """User search history"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        from .models import SearchHistory
        return SearchHistory.objects.filter(user=self.request.user).order_by('-created_at')[:50]
    
    def get_serializer_class(self):
        from .serializers import SearchHistorySerializer
        return SearchHistorySerializer
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear search history"""
        from .models import SearchHistory
        count = SearchHistory.objects.filter(user=request.user).delete()[0]
        return Response({'message': f'{count} search history items deleted'})
