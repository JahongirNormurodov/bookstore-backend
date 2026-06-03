# 🚀 Quick Start Guide

## Loyihani ishga tushirish (5 daqiqada)

### 1. Serverni ishga tushiring

```bash
cd /Users/macbookair/Desktop/Django/bookstore-backend
source .venv/bin/activate
python manage.py runserver
```

### 2. Admin panelga kiring

URL: http://localhost:8000/admin/

Superuser yaratish (agar yo'q bo'lsa):
```bash
python manage.py createsuperuser
```

### 3. Ma'lumotlar kiritish

Admin panelda quyidagilarni yarating:

#### 1️⃣ Janr qo'shish
**Books → Genres → Add Genre**
- Name: Badiy adabiyot
- Slug: badiy-adabiyot (avtomatik)

#### 2️⃣ Muallif qo'shish
**Books → Authors → Add Author**
- Name: O'tkir Hoshimov
- Birth date: 1941-08-10

#### 3️⃣ Nashriyot qo'shish
**Books → Publishers → Add Publisher**
- Name: Sharq
- Country: O'zbekiston

#### 4️⃣ Kitob qo'shish
**Books → Books → Add Book**
- Title: Dunyoning ishlari
- Slug: dunyoning-ishlari (avtomatik)
- ISBN: 978-9943-123-45-6
- Author: O'tkir Hoshimov
- Genre: Badiy adabiyot
- Publisher: Sharq
- Price: 50000
- Language: uz
- Page count: 350
- Is active: ✓

#### 5️⃣ Kitob nusxalari qo'shish
**Books → Book copies → Add Book copy**
- Book: Dunyoning ishlari
- Copy code: BK-001-01
- Status: Yaxshi (good)
- Barcode: 1234567890

Bir nechta nusxa qo'shing (BK-001-02, BK-001-03...)

#### 6️⃣ Obuna tarifi yaratish
**Subscriptions → Subscription plans → Add**
- Name: Basic
- Slug: basic
- Price monthly: 50000
- Max books per month: 2
- Max simultaneous books: 1

Premium tarif ham yarating:
- Name: Premium
- Slug: premium
- Price monthly: 150000
- Max books per month: unlimited
- Max simultaneous books: 3
- Is unlimited: ✓

#### 7️⃣ Foydalanuvchi yaratish
**Users → Users → Add User**
- Phone: +998901234567
- Email: user@example.com
- First name: Ali
- Last name: Valiyev
- Password: (o'rnating)

Keyin Profile yarating (inline):
- Passport number: AA1234567
- Birth date: 1990-01-01
- Is phone verified: ✓
- Is passport verified: ✓

---

## 📊 Tizimni sinab ko'rish

### Test scenario:

#### 1. Ijara yaratish
**Rentals → Rentals → Add Rental**
- User: Ali Valiyev
- Book copy: BK-001-01
- Status: Active
- Due date: (bugundan 7 kun keyin)
- Rental price: 17500 (haftalik)
- Deposit amount: 50000

#### 2. To'lov yaratish
**Payments → Payments → Add Payment**
- User: Ali Valiyev
- Amount: 17500
- Payment type: Ijara to'lovi
- Payment method: Karta
- Status: To'langan
- Rental: (yuqoridagi ijara)

#### 3. Wishlist qo'shish
**Users → Wishlists → Add Wishlist**
- User: Ali Valiyev
- Book: Dunyoning ishlari

#### 4. Trust score qo'shish
**Users → Trust scores → Add**
- User: Ali Valiyev
- Score: +5
- Reason: O'z vaqtida qaytarish bonusi

---

## 🎯 Admin paneldagi barcha bo'limlar

### 📚 Books (Kitoblar)
- Genres (Janrlar)
- Authors (Mualliflar)
- Publishers (Nashriyotlar)
- Books (Kitoblar)
- Book copies (Kitob nusxalari)
- Book reviews (Sharhlar)
- Similar books (O'xshash kitoblar)

### 👥 Users (Foydalanuvchilar)
- Users (Foydalanuvchilar)
- Profiles (Profillar)
- Trust scores (Ishonchlilik darajalari)
- OTP codes (Tasdiqlash kodlari)
- Wishlists (Sevimlilar)
- Search histories (Qidiruv tarixi)
- Referral codes (Referral kodlari)
- Referrals (Referrallar)
- Loyalty points (Bonus ballar)

### 📖 Rentals (Ijaralar)
- Rentals (Ijaralar)
- Rental extensions (Uzaytirishlar)

### 🎫 Subscriptions (Obunalar)
- Subscription plans (Tarif rejalari)
- Subscriptions (Obunalar)

### 💳 Payments (To'lovlar)
- Payments (To'lovlar)
- Penalties (Jarimalar)

### 🔔 Notifications (Bildirishnomalar)
- Notifications (Bildirishnomalar)

### 📋 Queues (Navbatlar)
- Book queues (Kitob navbatlari)
- Book notifications (Kitob xabarnomalar)

### 🚗 Couriers (Kuryerlar)
- Couriers (Kuryerlar)
- Deliveries (Yetkazib berishlar)

### ⚙️ Admin Panel
- Staff roles (Xodim rollari)
- Staff members (Xodimlar)
- Activity logs (Faoliyat loglari)
- Blog posts (Blog postlari)
- FAQs (Savollar)

---

## 🔍 Foydali admin filtrlar

### Faol ijaralar
**Rentals → Rentals**
- Status filter: Active

### Kechikkan ijaralar
Rentals ro'yxatida due_date bugundan oldingilar

### Mavjud kitoblar
**Books → Book copies**
- Status filter: Yaxshi / Yangi
- (Faol ijarada bo'lmaganlar)

### Blacklist foydalanuvchilar
**Users → Profiles**
- Is blacklisted filter: Yes

### To'lanmagan jarimalar
**Payments → Penalties**
- Is paid filter: No

---

## 📱 API (Keyingi bosqich)

API hali to'liq tayyor emas, lekin asoslar mavjud:

```bash
# API schema
http://localhost:8000/api/schema/swagger-ui/
http://localhost:8000/api/schema/redoc/

# Kitoblar
http://localhost:8000/api/books/

# Notifications
http://localhost:8000/api/notifications/
```

---

## 🐛 Debugging

### Migration muammolari
```bash
# Barcha migratsiyalarni ko'rish
python manage.py showmigrations

# Migrate qilish
python manage.py migrate

# Muammo bo'lsa, barcha migratsiyalarni qayta qilish
python manage.py migrate --fake-initial
```

### Ma'lumotlar bazasini tozalash
```bash
python manage.py flush
```

### Yangi superuser
```bash
python manage.py createsuperuser
```

---

## ✅ To-do list (Admin bilan ishlash uchun)

- [ ] 5+ kitob qo'shing
- [ ] Har bir kitobning 2-3 nusxasini qo'shing
- [ ] 3+ foydalanuvchi yarating
- [ ] 2-3 ta faol ijara yarating
- [ ] Wishlist va qidiruv tarixini test qiling
- [ ] Obuna tariflarini sozlang
- [ ] Blog post yozing
- [ ] FAQ qo'shing

---

## 🎉 Tayyor!

Admin panel orqali to'liq ishlaydigan kitob ijarasi tizimi tayyor. Keyingi bosqich - API endpointlarni yaratish va frontend bilan bog'lash.

**Happy coding! 🚀**
