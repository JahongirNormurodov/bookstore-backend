# 📡 API Endpoints Documentation

Base URL: `http://localhost:8000/api/v1`

## 🔐 Authentication Endpoints

### Login
```http
POST /users/login/
Content-Type: application/json

{
  "phone": "+998901234567",
  "password": "your_password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Logout
```http
POST /users/logout/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Token Refresh
```http
POST /users/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access": "new_access_token"
}
```

---

## 👤 User Endpoints

### Register
```http
POST /users/users/register/
Content-Type: application/json

{
  "phone": "+998901234567",
  "email": "user@example.com",
  "first_name": "Ali",
  "last_name": "Valiyev",
  "password": "securepassword123",
  "confirm_password": "securepassword123"
}
```

### Send OTP Code
```http
POST /users/users/send-code/
Content-Type: application/json

{
  "phone": "+998901234567",
  "purpose": "register"  // or "login", "reset_password"
}
```

### Verify OTP Code
```http
POST /users/users/verify-code/
Content-Type: application/json

{
  "phone": "+998901234567",
  "code": "123456",
  "purpose": "register"
}
```

### Get Current User
```http
GET /users/users/me/
Authorization: Bearer {access_token}
```

### Update Current User
```http
PATCH /users/users/update-me/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "first_name": "New Name",
  "profile": {
    "address": "Tashkent, Uzbekistan",
    "birth_date": "1990-01-01"
  }
}
```

---

## 📚 Books Endpoints

### List Books
```http
GET /books/?search=dunyoning&genre__slug=badiy-adabiyot&ordering=-rating
Authorization: Bearer {access_token}

Query Parameters:
- search: Search by title, author, ISBN
- genre__slug: Filter by genre
- author__id: Filter by author
- language: Filter by language
- is_active: Filter by active status
- ordering: Sort by (title, -created_at, rating, price)
```

### Get Book Detail
```http
GET /books/{book_id}/
Authorization: Bearer {access_token}
```

### Get Book Reviews
```http
GET /books/{book_id}/reviews/
Authorization: Bearer {access_token}
```

### Add Book Review
```http
POST /books/{book_id}/add_review/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "rating": 5,
  "review_text": "Juda ajoyib kitob!"
}
```

---

## 💝 Wishlist Endpoints

### List Wishlist
```http
GET /users/wishlist/
Authorization: Bearer {access_token}
```

### Add to Wishlist
```http
POST /users/wishlist/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "book": "book_uuid_here"
}
```

### Remove from Wishlist
```http
DELETE /users/wishlist/{wishlist_id}/
Authorization: Bearer {access_token}
```

### Clear Wishlist
```http
DELETE /users/wishlist/clear/
Authorization: Bearer {access_token}
```

---

## 📖 Rental Endpoints

### List Rentals
```http
GET /rentals/?status=active
Authorization: Bearer {access_token}

Query Parameters:
- status: pending, active, overdue, returned, cancelled
- user: Filter by user (admin only)
```

### Create Rental
```http
POST /rentals/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "book_copy": "copy_uuid_here",
  "rental_days": 7,
  "delivery_address": "Tashkent, Amir Temur 15"
}
```

### Get My Active Rentals
```http
GET /rentals/my_rentals/
Authorization: Bearer {access_token}
```

### Extend Rental
```http
POST /rentals/{rental_id}/extend/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "additional_days": 7
}
```

### Return Book
```http
POST /rentals/{rental_id}/return/
Authorization: Bearer {access_token}
```

---

## 🎫 Subscription Endpoints

### List Subscription Plans
```http
GET /subscriptions/plans/
```

### Get Active Subscription
```http
GET /subscriptions/my_subscription/
Authorization: Bearer {access_token}
```

### Subscribe to Plan
```http
POST /subscriptions/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "plan": "plan_uuid_here"
}
```

### Cancel Subscription
```http
POST /subscriptions/{subscription_id}/cancel/
Authorization: Bearer {access_token}
```

---

## 💳 Payment Endpoints

### List Payments
```http
GET /payments/payments/?payment_type=rental&status=completed
Authorization: Bearer {access_token}

Query Parameters:
- payment_type: rental, deposit, penalty, subscription, refund
- payment_method: cash, card, payme, click, uzum
- status: pending, completed, failed, refunded
```

### Get My Payments
```http
GET /payments/payments/my_payments/
Authorization: Bearer {access_token}
```

### Create Payment
```http
POST /payments/payments/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "amount": "50000.00",
  "payment_type": "rental",
  "payment_method": "card",
  "rental": "rental_uuid_here"
}
```

### Get Payment Statistics (Admin)
```http
GET /payments/payments/statistics/
Authorization: Bearer {admin_token}
```

---

## 📋 Queue Endpoints

### List Book Queues
```http
GET /queues/queues/?status=waiting
Authorization: Bearer {access_token}

Query Parameters:
- status: waiting, notified, fulfilled, cancelled, expired
- book: Filter by book
```

### Get My Queue
```http
GET /queues/queues/my_queue/
Authorization: Bearer {access_token}
```

### Join Queue
```http
POST /queues/queues/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "book": "book_uuid_here"
}
```

### Cancel Queue Entry
```http
POST /queues/queues/{queue_id}/cancel/
Authorization: Bearer {access_token}
```

### List Book Notifications
```http
GET /queues/notifications/
Authorization: Bearer {access_token}
```

### Subscribe to Book Notification
```http
POST /queues/notifications/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "book": "book_uuid_here"
}
```

### Unsubscribe from Notification
```http
DELETE /queues/notifications/{notification_id}/unsubscribe/
Authorization: Bearer {access_token}
```

---

## 🔔 Notification Endpoints

### List Notifications
```http
GET /notifications/?is_read=false
Authorization: Bearer {access_token}

Query Parameters:
- is_read: true/false
- notification_type: rental_reminder, overdue, etc.
```

### Mark as Read
```http
POST /notifications/{notification_id}/mark_read/
Authorization: Bearer {access_token}
```

### Mark All as Read
```http
POST /notifications/mark_all_read/
Authorization: Bearer {access_token}
```

### Get Unread Count
```http
GET /notifications/unread_count/
Authorization: Bearer {access_token}
```

---

## 🎯 Loyalty Points Endpoints

### Get Loyalty Points History
```http
GET /users/loyalty-points/
Authorization: Bearer {access_token}
```

### Get Current Balance
```http
GET /users/loyalty-points/balance/
Authorization: Bearer {access_token}

Response:
{
  "balance": 15000
}
```

---

## 🏆 Trust Score Endpoints

### Get Trust Score History
```http
GET /users/trust-scores/
Authorization: Bearer {access_token}
```

### Get Current Trust Score
```http
GET /users/trust-scores/current/
Authorization: Bearer {access_token}

Response:
{
  "trust_score": 105
}
```

---

## 🔍 Search History Endpoints

### Get Search History
```http
GET /users/search-history/
Authorization: Bearer {access_token}
```

### Clear Search History
```http
DELETE /users/search-history/clear/
Authorization: Bearer {access_token}
```

---

## 📊 Penalty Endpoints

### List Penalties
```http
GET /payments/penalties/?is_paid=false
Authorization: Bearer {access_token}

Query Parameters:
- is_paid: true/false
- rental__user: Filter by user (admin only)
```

### Mark Penalty as Paid
```http
POST /payments/penalties/{penalty_id}/mark_paid/
Authorization: Bearer {access_token}
```

---

## 📖 API Documentation

### Swagger UI
```
http://localhost:8000/api/docs/
```

### ReDoc
```
http://localhost:8000/api/redoc/
```

### OpenAPI Schema
```
http://localhost:8000/api/schema/
```

---

## 🔑 Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

Get your token by logging in via `/users/login/` endpoint.

---

## 📝 Response Format

### Success Response
```json
{
  "id": "uuid",
  "field1": "value1",
  "field2": "value2",
  ...
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": {
    "field": ["Error details"]
  }
}
```

### Paginated Response
```json
{
  "count": 100,
  "next": "http://api.example.com/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 🚀 Quick Start

1. **Register a new user:**
```bash
curl -X POST http://localhost:8000/api/v1/users/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+998901234567",
    "email": "user@example.com",
    "first_name": "Ali",
    "last_name": "Valiyev",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

2. **Login:**
```bash
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+998901234567",
    "password": "password123"
  }'
```

3. **Get books:**
```bash
curl -X GET http://localhost:8000/api/v1/books/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🛠 Development Tools

### Seed Sample Data
```bash
python manage.py seed_books
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Server
```bash
python manage.py runserver
```

---

**For more details, visit the Swagger documentation at `/api/docs/`**
