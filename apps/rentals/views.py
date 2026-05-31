# rentals/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from .models import Rental, RentalExtension
from .serializers import RentalSerializer, RentalCreateSerializer, RentalExtensionSerializer
from .choices import RentalStatus


class RentalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['destroy', 'update']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Rental.objects
            .select_related(
                'user',
                'book_copy__book__publisher',
                'book_copy__book__author',
                'book_copy__book__genre'
            )
            .prefetch_related('extensions')
        )
        if user.is_staff:
            return qs
        return qs.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return RentalCreateSerializer
        if self.action == 'extend':
            return RentalExtensionSerializer
        return RentalSerializer

    def perform_create(self, serializer):
        book_copy = serializer.validated_data.get('book_copy')

        # book_copy mavjudligini tekshirish
        if not book_copy.is_available:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Bu kitob nusxasi hozir mavjud emas.")

        # book_copy ni band qilish
        book_copy.is_available = False
        book_copy.save(update_fields=['is_available'])

        serializer.save(
            user=self.request.user,
            status=RentalStatus.PENDING
        )

    # POST /rentals/{id}/return/
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        rental = self.get_object()

        if rental.status not in [RentalStatus.ACTIVE, RentalStatus.OVERDUE]:
            return Response(
                {"error": "Faqat faol ijarani qaytarish mumkin."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kitob nusxasini bo'shatish
        rental.book_copy.is_available = True
        rental.book_copy.save(update_fields=['is_available'])

        rental.status      = RentalStatus.RETURNED
        rental.returned_at = timezone.now()
        rental.save(update_fields=['status', 'returned_at'])

        return Response(
            {"message": "Kitob muvaffaqiyatli qaytarildi."},
            status=status.HTTP_200_OK
        )

    # POST /rentals/{id}/extend/
    @action(detail=True, methods=['post'])
    def extend(self, request, pk=None):
        rental = self.get_object()

        if rental.status not in [RentalStatus.ACTIVE, RentalStatus.OVERDUE]:
            return Response(
                {"error": "Faqat faol ijarani uzaytirish mumkin."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RentalExtensionSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(
                rental=rental,
                approved_by=request.user if request.user.is_staff else None
            )
            # extended_days ni yangilash
            rental.extended_days += serializer.validated_data['extended_by_days']
            rental.due_date       = serializer.validated_data['new_due_date']
            rental.save(update_fields=['extended_days', 'due_date'])

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
