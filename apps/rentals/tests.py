# rentals/tests.py
from datetime import timedelta
from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.users.models import User
from apps.books.models import Book, BookCopy
from apps.rentals.models import Rental
from apps.rentals.choices import RentalStatus
from apps.payments.models import Penalty


class RentalFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='+998901112233',
            email='renter@example.com',
            password='pass12345',
            first_name='Renter',
            last_name='Test',
        )
        self.book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            isbn='ISBN-TEST-001',
            price=Decimal('100000.00'),
            is_active=True,
        )
        self.copy = BookCopy.objects.create(
            book=self.book,
            copy_code='BK-TEST-01',
            status=BookCopy.Status.GOOD,
        )
        self.client.force_authenticate(self.user)

    def test_create_rental_sets_price_and_deposit(self):
        """Regression: rental_price/deposit_amount serverda hisoblanishi kerak
        (avval NOT NULL IntegrityError bilan crash bo'lardi)."""
        due = timezone.now().date() + timedelta(days=7)
        resp = self.client.post('/api/v1/rentals/', {
            'book_copy': str(self.copy.id),
            'due_date': due.isoformat(),
        }, format='json')

        self.assertEqual(resp.status_code, 201, resp.data)
        rental = Rental.objects.get(user=self.user)
        self.assertEqual(rental.status, RentalStatus.ACTIVE)
        self.assertGreater(rental.rental_price, 0)
        self.assertEqual(rental.deposit_amount, self.book.deposit_amount)

    def test_cannot_rent_unavailable_copy(self):
        due = timezone.now().date() + timedelta(days=7)
        # Birinchi ijara nusxani band qiladi
        Rental.objects.create(
            user=self.user, book_copy=self.copy, status=RentalStatus.ACTIVE,
            due_date=due, rental_price=Decimal('1000'), deposit_amount=Decimal('100000'),
        )
        resp = self.client.post('/api/v1/rentals/', {
            'book_copy': str(self.copy.id),
            'due_date': due.isoformat(),
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_return_overdue_creates_penalty(self):
        """Muddati o'tgan ijara qaytarilganda jarima yaratilishi kerak."""
        overdue_due = timezone.now().date() - timedelta(days=3)
        rental = Rental.objects.create(
            user=self.user, book_copy=self.copy, status=RentalStatus.ACTIVE,
            due_date=overdue_due, rental_price=Decimal('1000'),
            deposit_amount=Decimal('100000'),
        )
        resp = self.client.post(f'/api/v1/rentals/{rental.id}/return_book/', format='json')
        self.assertEqual(resp.status_code, 200, resp.data)
        rental.refresh_from_db()
        self.assertEqual(rental.status, RentalStatus.RETURNED)
        self.assertTrue(Penalty.objects.filter(rental=rental).exists())
        # Jarima bo'lgani uchun garov qaytarilmaydi
        self.assertFalse(rental.deposit_returned)

    def test_return_on_time_returns_deposit(self):
        due = timezone.now().date() + timedelta(days=3)
        rental = Rental.objects.create(
            user=self.user, book_copy=self.copy, status=RentalStatus.ACTIVE,
            due_date=due, rental_price=Decimal('1000'),
            deposit_amount=Decimal('100000'),
        )
        resp = self.client.post(f'/api/v1/rentals/{rental.id}/return_book/', format='json')
        self.assertEqual(resp.status_code, 200, resp.data)
        rental.refresh_from_db()
        self.assertEqual(rental.status, RentalStatus.RETURNED)
        self.assertTrue(rental.deposit_returned)
        self.assertFalse(Penalty.objects.filter(rental=rental).exists())
