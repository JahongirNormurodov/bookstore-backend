New project structure (Django + DRF)

bookstore-backend/
├── bookstore/                  # Asosiy Django project
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   │   └── __init__.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                       # Barcha ilovalar (modullar)
│   ├── users/                  # Foydalanuvchilar, profil, trust score
│   ├── books/                  # Kitoblar va kategoriyalar
│   ├── copies/                 # Har bir kitob nusxasi (inventory)
│   ├── rentals/                # Ijaralar, muddat, penalti
│   ├── subscriptions/          # Obuna tizimi
│   ├── notifications/          # Bildirishnomalar
│   ├── payments/               # To'lovlar
│   ├── queues/                 # Navbat tizimi
│   ├── core/                   # Umumiy (models, managers, utils)
│   ├── admin_panel/            # Admin uchun maxsus logic
│   └── couriers/               # Kuryer paneli
│
├── config/                     # Konfiguratsiyalar
├── utils/                      # Yordamchi funksiyalar
├── templates/                  # Agar kerak bo'lsa
├── static/
├── media/
├── prisma/                     # (ixtiyoriy, lekin biz Django ORM ishlatamiz)
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
-----------------------------------------------------------------------------------------------------
Structure inside every app (for example: rentals/)
rentals/
├── migrations/
├── __init__.py
├── admin.py
├── models.py
├── serializers.py
├── views.py
├── urls.py
├── services.py          # Murakkab biznes logika
├── tasks.py             # Celery tasks (penalti, eslatmalar)
├── signals.py
├── permissions.py
├── tests/
│   ├── test_models.py
│   └── test_views.py
└── apps.py

Used tecknologies 

