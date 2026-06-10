# users/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, OTPCode, Wishlist, LoyaltyPoints, TrustScore, SearchHistory
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserRegistrationSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    WishlistSerializer,
    WishlistCreateSerializer,
    LoyaltyPointsSerializer,
    TrustScoreSerializer,
    SearchHistorySerializer,
)
from .services import send_verification_sms


class LoginView(TokenObtainPairView):
    """Telefon + parol -> JWT token"""
    permission_classes = [AllowAny]
    throttle_scope = 'login'


class LogoutView(APIView):
    """Refresh tokenni blacklist qilish"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
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


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # drf-spectacular schema generatsiyasi anonymous user bilan chaqiradi
        if getattr(self, 'swagger_fake_view', False) or not user.is_authenticated:
            return User.objects.none()
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
        # Har bir sezgir action uchun alohida throttle scope
        scopes = {
            'register':    'register',
            'send_code':   'send_otp',
            'verify_code': 'verify_otp',
        }
        if self.action in scopes:
            self.throttle_scope = scopes[self.action]
        return super().get_throttles()

    # POST /api/v1/users/users/register/
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                send_verification_sms(
                    phone=user.phone,
                    purpose=OTPCode.Purpose.REGISTER
                )
            except Exception:
                pass  # SMS yetkazilmasa ham ro'yxatdan o'tish muvaffaqiyatli
            return Response(
                {
                    "message": "Ro'yxatdan o'tdingiz. Telefonga kod yuborildi.",
                    "phone": user.phone,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # POST /api/v1/users/users/send-code/
    @action(detail=False, methods=['post'], url_path='send-code')
    def send_code(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']
        purpose = serializer.validated_data.get('purpose', OTPCode.Purpose.REGISTER)

        # User enumeration oldini olish: raqam ro'yxatda bo'lsin/bo'lmasin
        # bir xil generic javob qaytaramiz.
        try:
            send_verification_sms(phone=phone, purpose=purpose)
        except Exception:
            pass

        return Response(
            {"message": "Agar raqam ro'yxatdan o'tgan bo'lsa, tasdiqlash kodi yuborildi."},
            status=status.HTTP_200_OK
        )

    # POST /api/v1/users/users/verify-code/
    @action(detail=False, methods=['post'], url_path='verify-code')
    def verify_code(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        otp = serializer.validated_data['otp']
        purpose = serializer.validated_data['purpose']

        otp.verify()

        if purpose == OTPCode.Purpose.REGISTER:
            profile = user.profile
            profile.is_phone_verified = True
            profile.save(update_fields=['is_phone_verified'])

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Telefon tasdiqlandi.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK
            )

        if purpose == OTPCode.Purpose.RESET_PASSWORD:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Kod tasdiqlandi. Yangi parol o'rnating.",
                    "reset_token": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

        return Response({"message": "Kod tasdiqlandi."}, status=status.HTTP_200_OK)

    # GET /api/v1/users/users/me/
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    # PATCH /api/v1/users/users/update-me/
    @action(detail=False, methods=['patch'], url_path='update-me')
    def update_me(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # POST /api/v1/users/users/logout/
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
            return Response({"message": "Muvaffaqiyatli chiqildi."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token yaroqsiz."}, status=status.HTTP_400_BAD_REQUEST)


class WishlistViewSet(viewsets.ModelViewSet):
    """Foydalanuvchi wishlist boshqaruvi"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Wishlist.objects.none()
        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related('book', 'book__author')

    def get_serializer_class(self):
        if self.action == 'create':
            return WishlistCreateSerializer
        return WishlistSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        count = self.get_queryset().delete()[0]
        return Response({'message': f'{count} ta kitob wishlistdan olib tashlandi'})


class LoyaltyPointsViewSet(viewsets.ReadOnlyModelViewSet):
    """Bonus ballar tarixi"""
    permission_classes = [IsAuthenticated]
    serializer_class = LoyaltyPointsSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return LoyaltyPoints.objects.none()
        return LoyaltyPoints.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def balance(self, request):
        return Response({'balance': request.user.total_loyalty_points})


class TrustScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """Ishonchlilik darajasi tarixi"""
    permission_classes = [IsAuthenticated]
    serializer_class = TrustScoreSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return TrustScore.objects.none()
        if self.request.user.is_staff:
            return TrustScore.objects.select_related('user', 'changed_by').all()
        return TrustScore.objects.filter(user=self.request.user).select_related('changed_by')

    @action(detail=False, methods=['get'])
    def current(self, request):
        return Response({'trust_score': request.user.current_trust_score})


class SearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Qidiruv tarixi"""
    permission_classes = [IsAuthenticated]
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return SearchHistory.objects.none()
        return SearchHistory.objects.filter(user=self.request.user).order_by('-created_at')[:50]

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        count = SearchHistory.objects.filter(user=request.user).delete()[0]
        return Response({'message': f'{count} ta qidiruv tarixi o\'chirildi'})
