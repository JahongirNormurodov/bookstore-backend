# rentals/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from apps.books.models import BookCopy
from apps.payments.models import Penalty
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
        if getattr(self, 'swagger_fake_view', False) or not user.is_authenticated:
            return Rental.objects.none()
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
        due_date = serializer.validated_data.get('due_date')

        # Bir nusxa uchun race-condition oldini olish: qatorni qulflaymiz
        with transaction.atomic():
            locked_copy = BookCopy.objects.select_for_update().get(pk=book_copy.pk)

            if not locked_copy.is_available:
                raise ValidationError("Bu kitob nusxasi hozir mavjud emas.")

            days = (due_date - timezone.now().date()).days
            book = locked_copy.book
            rental_price = book.calculate_rental_price(days)
            deposit_amount = book.deposit_amount

            # rental_price va deposit_amount serverda hisoblanadi —
            # mijoz tomonidan yuborilmaydi.
            serializer.save(
                user=self.request.user,
                status=RentalStatus.ACTIVE,
                rented_at=timezone.now(),
                rental_price=rental_price,
                deposit_amount=deposit_amount,
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

        with transaction.atomic():
            today = timezone.now().date()
            penalty_amount = 0

            # Kech qaytarish jarimasi
            if today > rental.due_date:
                days_overdue = (today - rental.due_date).days
                daily_penalty = rental.book_copy.book.rental_price_daily
                penalty_amount = daily_penalty * days_overdue
                Penalty.objects.create(
                    rental=rental,
                    days_overdue=days_overdue,
                    penalty_amount=penalty_amount,
                    is_paid=False,
                )

            rental.status = RentalStatus.RETURNED
            rental.returned_at = timezone.now()

            # Jarima bo'lmasa garov qaytariladi
            if penalty_amount == 0:
                rental.deposit_returned = True
                rental.deposit_returned_at = timezone.now()
                rental.save(update_fields=[
                    'status', 'returned_at', 'deposit_returned', 'deposit_returned_at'
                ])
            else:
                rental.save(update_fields=['status', 'returned_at'])

            # Nusxaning ijara hisobini oshirish
            copy = rental.book_copy
            copy.rental_count = (copy.rental_count or 0) + 1
            copy.save(update_fields=['rental_count'])

        message = "Kitob muvaffaqiyatli qaytarildi."
        if penalty_amount:
            message += f" Kechikkan kunlar uchun {penalty_amount} so'm jarima qo'llanildi."

        return Response(
            {"message": message, "penalty_amount": str(penalty_amount)},
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
            with transaction.atomic():
                new_due_date = serializer.validated_data['new_due_date']
                extra_days = (new_due_date - rental.due_date).days

                serializer.save(
                    rental=rental,
                    approved_by=request.user if request.user.is_staff else None
                )

                # Qo'shimcha kunlar uchun narx hisoblanadi
                if extra_days > 0:
                    extra_charge = rental.book_copy.book.calculate_rental_price(extra_days)
                    rental.rental_price = rental.rental_price + extra_charge

                rental.extended_days += serializer.validated_data['extended_by_days']
                rental.due_date = new_due_date
                rental.save(update_fields=['extended_days', 'due_date', 'rental_price'])

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
