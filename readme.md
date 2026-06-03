# BOOKstore — Kitob Ijarasi Xizmati (Book Rental Service)

Raqamli kutubxona - kitoblarni ijaraga berish tizimi.

## 📋 Loyiha haqida

Bu loyiha kitoblarni sotish emas, balki **ijaraga berish** xizmatini taqdim etadi. Foydalanuvchilar kitoblarni ma'lum muddat uchun ijaraga olib, garov to'laydilar va muddatida qaytarishlari kerak.

## ✨ Asosiy xususiyatlar

### 👤 Foydalanuvchi qismi

#### Ro'yxat va profil
- ✅ Telefon/email orqali ro'yxatdan o'tish
- ✅ SMS/email tasdiqlash (OTP)
- ✅ Pasport ma'lumotlari (ijaraga olish uchun majburiy)
- ✅ Shaxsiy kabinet
- ✅ Ishonchlilik darajasi (trust score) - o'z vaqtida qaytarsa oshib boradi
- ✅ Blacklist tizimi

#### Katalog va qidiruv
- ✅ Janrlar bo'yicha katalog
- ✅ Mualliflar bo'yicha katalog
- ✅ Til bo'yicha katalog
- ✅ Filtrlar (janr, til, reyting, yil, mavjudlik)
- ✅ Saralash (mashhurligi, yangiligi, reyting, ijara narxi)
- ✅ Qidiruv (title, author, ISBN)
- ✅ Qidiruv tarixi

#### Kitob sahifasi
- ✅ Muqovaning bir nechta rasmi (4 tagacha)
- ✅ Kitob preview (bir necha sahifa)
- ✅ Batafsil ma'lumot
- ✅ Reyting va sharhlar
- ✅ Ijara narxi (kunlik / haftalik / oylik)
- ✅ Garov summasi
- ✅ Hozir nechta nusxa mavjud
- ✅ Band bo'lsa — qachon bo'shashi
- ✅ "Bo'shaganda xabar bering" tugmasi
- ✅ Navbatga turish (queue) — band kitob uchun
- ✅ O'xshash kitoblar
- ✅ Shu muallifning boshqa kitoblari

#### Ijara muddati
- ✅ Standart muddatlar: 3 kun, 1 hafta, 2 hafta, 1 oy
- ✅ O'z muddatini tanlash (kunlar bo'yicha)
- ✅ Muddatga qarab narx avtomatik hisoblanadi
- ✅ Maksimal ijara muddati (60 kun)
- ✅ Bir vaqtda nechta kitob olish mumkinligi (limit)

#### Obuna (Subscription)
- ✅ Oylik obuna tariflari:
  - Basic: oyiga 2 ta kitob
  - Standard: oyiga 4 ta kitob
  - Premium: cheksiz kitob (bir vaqtda 3 tagacha)
- ✅ Obunani to'xtatish / qayta tiklash
- ✅ Avtomatik yangilanish

#### Mening ijaralarim
- ✅ Faol ijaradagi kitoblar
- ✅ Har biri uchun qaytarish muddati va qolgan kunlar
- ✅ Muddatni uzaytirish
- ✅ Ijara tarixi
- ✅ Sharh qoldirish (qaytargandan keyin)

#### Kech qaytarish (Penaltilar)
- ✅ Muddat tugashidan oldin eslatmalar
- ✅ Muddat tugagandan keyin har kunlik penalti
- ✅ Garov to'liq ushlab qolinishi
- ✅ Kitob qaytarilmasa — to'liq narx undiriladi

#### Bonus va loyallik
- ✅ Cashback / ball tizimi (har ijaradan)
- ✅ Ballarni keyingi ijarada ishlatish
- ✅ Referral dasturi (do'stni taklif qil)
- ✅ Ishonchlilik darajasi
- ✅ Tug'ilgan kun chegirmasi

#### Bildirishnomalar
- ✅ Push-notification
- ✅ Email / Telegram bot ready
- ✅ Qaytarish kuni yaqinlashayotgani
- ✅ Garov qaytarildi
- ✅ Yangi kitoblar
- ✅ Navbatdagi kitob bo'shadi
- ✅ Obuna tugashi yaqin

#### Boshqa
- ✅ Wishlist (sevimlilar)
- ✅ Qidiruv tarixi

### 🛠 Admin panel

#### Dashboard
- ✅ Faol ijaralar soni
- ✅ Bugun qaytarilishi kerak bo'lganlar
- ✅ Kechikkan ijaralar
- ✅ Eng ko'p ijaraga olinayotgan kitoblar

#### Kitoblar boshqaruvi (Ombor)
- ✅ Kitob qo'shish (har bir nusxa alohida ID bilan)
- ✅ Bir nomdagi kitobning bir nechta nusxasi
- ✅ Har bir nusxa holati (yangi, yaxshi, o'rtacha, eskirgan, yo'qolgan)
- ✅ Hozir kimda ekanligi
- ✅ Ijara tarixi (har bir nusxa qancha marta ijaraga ketgan)
- ✅ Foydalanish darajasi
- ✅ Barcode/QR-kod

#### Ijara boshqaruvi
- ✅ Faol ijaralar ro'yxati
- ✅ Statusni o'zgartirish
- ✅ Muddatni uzaytirish (qo'lda)
- ✅ Penaltini bekor qilish
- ✅ Bahsli holatlarni hal qilish

#### Mijozlar
- ✅ Mijozlar bazasi
- ✅ Verifikatsiya (pasport tasdiqlash)
- ✅ Ishonchlilik darajasi
- ✅ Ijara tarixi
- ✅ Qora ro'yxat (blacklist)

#### Obunalar
- ✅ Obuna tariflarini boshqarish
- ✅ Faol obunalar
- ✅ Bekor qilingan obunalar

#### Kontent
- ✅ Janrlar, mualliflar, nashriyotlar
- ✅ Blog
- ✅ FAQ

#### Kuryer paneli
- ✅ Bugungi marshrutlar
- ✅ Olib boriladigan va olib kelinadigan kitoblar
- ✅ Foto yuklash (kitob holati)
- ✅ Mijoz imzosi (elektron)

#### Hisobotlar
- ✅ Daromad (kun/hafta/oy) ready models
- ✅ Eng faol mijozlar
- ✅ Eng faol kitoblar
- ✅ Yo'qotishlar
- ✅ Obuna konversiyasi

#### Xodimlar va rollar
- ✅ Admin, menejer, kuryer, filial xodimi
- ✅ Har birining huquqlari
- ✅ Faoliyat loglari

## 🗂 Loyiha strukturasi

```
apps/
├── users/              # Foydalanuvchilar, profil, trust score, loyalty points
├── books/              # Kitoblar, mualliflar, janrlar, sharhlar
├── copies/             # Kitob nusxalari (har bir nusxa alohida)
├── rentals/            # Ijaralar, uzaytirish
├── subscriptions/      # Obuna tariflari va foydalanuvchi obunalari
├── notifications/      # Bildirishnomalar
├── payments/           # To'lovlar va jarimalar
├── queues/             # Kitob navbatlari
├── couriers/           # Kuryerlar va yetkazib berish
├── admin_panel/        # Admin panel, blog, FAQ, faoliyat loglari
└── common/             # Umumiy modellar va sozlamalar
```

## 🔧 Texnologiyalar

- **Backend**: Django 6.0+, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Filters**: django-filter
- **CORS**: django-cors-headers

## 🚀 O'rnatish

### 1. Repository'ni klonlash

```bash
git clone <repository-url>
cd bookstore-backend
```

### 2. Virtual environment yaratish

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
```

### 3. Bog'liqliklarni o'rnatish

```bash
pip install django djangorestframework django-cors-headers drf-spectacular django-filter djangorestframework-simplejwt python-dotenv psycopg2-binary pillow
```

### 4. Environment o'zgaruvchilari

`.env` fayl yarating:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=bookstore_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Database yaratish

```bash
# PostgreSQL'da database yaratish
createdb bookstore_db
```

### 6. Migratsiyalar

```bash
python manage.py migrate
```

### 7. Superuser yaratish

```bash
python manage.py createsuperuser
```

### 8. Serverni ishga tushirish

```bash
python manage.py runserver
```

## 📊 Modellar

### Users App
- **User**: Asosiy foydalanuvchi modeli
- **Profile**: Foydalanuvchi profili (pasport, avatar, blacklist)
- **TrustScore**: Ishonchlilik darajasi tarixi
- **OTPCode**: SMS/Email tasdiqlash kodlari
- **Wishlist**: Sevimli kitoblar
- **SearchHistory**: Qidiruv tarixi
- **ReferralCode**: Referral kodlari
- **Referral**: Referral tarixi
- **LoyaltyPoints**: Bonus ballar

### Books App
- **Book**: Kitoblar
- **Genre**: Janrlar
- **Author**: Mualliflar
- **Publisher**: Nashriyotlar
- **BookCopy**: Kitob nusxalari (har biri alohida ID bilan)
- **BookReview**: Kitob sharhlari va reytinglari
- **SimilarBook**: O'xshash kitoblar

### Rentals App
- **Rental**: Ijaralar
- **RentalExtension**: Ijara muddatini uzaytirish

### Subscriptions App
- **SubscriptionPlan**: Obuna tariflari
- **Subscription**: Foydalanuvchi obunalari

### Payments App
- **Payment**: To'lovlar (ijara, garov, jarima, obuna)
- **Penalty**: Kech qaytarish jarimalari

### Queues App
- **BookQueue**: Kitob navbatlari
- **BookNotification**: Kitob bo'shaganda xabar berish

### Couriers App
- **Courier**: Kuryerlar
- **Delivery**: Yetkazib berish

### Notifications App
- **Notification**: Bildirishnomalar

### Admin Panel App
- **StaffRole**: Xodim rollari
- **StaffMember**: Xodimlar
- **ActivityLog**: Faoliyat loglari
- **BlogPost**: Blog postlari
- **FAQ**: Ko'p so'raladigan savollar

## 🔗 API Endpoints

API dokumentatsiyasini ko'rish:

```
http://localhost:8000/api/schema/swagger-ui/
http://localhost:8000/api/schema/redoc/
```

## 📝 Keyingi qadamlar

1. ✅ Barcha modellar yaratildi
2. ✅ Admin panelda ro'yxatga olindi
3. ⏳ API viewlar va serializers yozish
4. ⏳ To'lov tizimini integratsiya qilish (Payme, Click, Uzum)
5. ⏳ SMS/Email xabarnomalar
6. ⏳ Telegram bot
7. ⏳ Celery tasks (eslatmalar, avtomatik jarimalar)
8. ⏳ Hisobotlar (daromad, statistika)
9. ⏳ Frontend (React/Vue.js)

## 📄 Litsenziya

MIT License

## 👨‍💻 Muallif

BookStore Backend Development Team
