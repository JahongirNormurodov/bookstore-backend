# payments/tests.py
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from rest_framework.test import APITestCase

from apps.users.models import User
from apps.books.models import Book, BookCopy
from apps.rentals.models import Rental
from apps.rentals.choices import RentalStatus
from apps.payments.models import Payment, Penalty


class PaymentSecurityTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            phone='+998900000001', email='alice@example.com',
            password='pass12345', first_name='Alice', last_name='A',
        )
        self.bob = User.objects.create_user(
            phone='+998900000002', email='bob@example.com',
            password='pass12345', first_name='Bob', last_name='B',
        )
        self.book = Book.objects.create(
            title='Sec Book', slug='sec-book', isbn='ISBN-SEC-1',
            price=Decimal('80000.00'), is_active=True,
        )
        self.copy = BookCopy.objects.create(
            book=self.book, copy_code='BK-SEC-01', status=BookCopy.Status.GOOD,
        )
        self.alice_rental = Rental.objects.create(
            user=self.alice, book_copy=self.copy, status=RentalStatus.ACTIVE,
            due_date=timezone.now().date() + timedelta(days=5),
            rental_price=Decimal('800'), deposit_amount=Decimal('80000'),
        )

    def test_payment_cannot_be_forged_for_another_user(self):
        """Bob o'z to'lovini Alice ijarasiga bog'lay olmasligi kerak (IDOR)."""
        self.client.force_authenticate(self.bob)
        resp = self.client.post('/api/v1/payments/payments/', {
            'payment_type': 'rental',
            'payment_method': 'card',
            'rental': str(self.alice_rental.id),
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_payment_amount_and_user_are_server_set(self):
        """Mijoz amount/status/user ni o'zi belgilay olmaydi."""
        self.client.force_authenticate(self.alice)
        resp = self.client.post('/api/v1/payments/payments/', {
            'payment_type': 'rental',
            'payment_method': 'card',
            'rental': str(self.alice_rental.id),
            'amount': '1',            # e'tiborga olinmasligi kerak
            'status': 'completed',    # e'tiborga olinmasligi kerak
            'user': str(self.bob.id), # e'tiborga olinmasligi kerak
        }, format='json')
        self.assertEqual(resp.status_code, 201, resp.data)
        payment = Payment.objects.get(user=self.alice, rental=self.alice_rental)
        self.assertEqual(payment.user_id, self.alice.id)
        self.assertEqual(payment.amount, self.alice_rental.rental_price)
        self.assertEqual(payment.status, Payment.PaymentStatus.PENDING)

    def test_user_cannot_clear_own_penalty(self):
        """Oddiy mijoz o'z jarimasini to'langan deb belgilay olmasligi kerak."""
        penalty = Penalty.objects.create(
            rental=self.alice_rental, days_overdue=2,
            penalty_amount=Decimal('2000'), is_paid=False,
        )
        self.client.force_authenticate(self.alice)
        resp = self.client.post(f'/api/v1/payments/penalties/{penalty.id}/mark_paid/', format='json')
        self.assertIn(resp.status_code, (403, 404))
        penalty.refresh_from_db()
        self.assertFalse(penalty.is_paid)


class WishlistSmokeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='+998900000009', email='w@example.com',
            password='pass12345', first_name='W', last_name='L',
        )

    def test_wishlist_list_does_not_500(self):
        """Regression: Wishlist import qilinmagani uchun 500 (NameError) bo'lardi."""
        self.client.force_authenticate(self.user)
        resp = self.client.get('/api/v1/users/wishlist/')
        self.assertEqual(resp.status_code, 200, resp.data)
