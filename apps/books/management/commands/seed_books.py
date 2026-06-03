# books/management/commands/seed_books.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.books.models import Genre, Author, Publisher, Book, BookCopy
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed database with sample books'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database with sample books...')

        # Create Genres
        genres_data = [
            ('Badiy adabiyot', 'Romanlar, hikoyalar va qissalar'),
            ('Ilmiy-ommabop', 'Ilm-fan va texnologiya haqida'),
            ('Biografiya', 'Mashhur shaxslar hayoti'),
            ('Tarix', 'Tarixiy voqealar va faktlar'),
            ('Bolalar adabiyoti', 'Bolalar uchun kitoblar'),
            ('Fantastika', 'Ilmiy fantastika va fantaziya'),
            ('Detektiv', 'Detektiv va jangari asarlar'),
            ('Psixologiya', 'Psixologiya va o\'z-o\'zini rivojlantirish'),
        ]

        genres = {}
        for name, description in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name), 'description': description}
            )
            genres[name] = genre
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created genre: {name}'))

        # Create Authors
        authors_data = [
            ('O\'tkir Hoshimov', 'O\'zbekistonning mashhur yozuvchisi', '1941-08-10'),
            ('Abdulla Qodiriy', 'O\'zbek klassik adabiyoti vakili', '1894-04-10'),
            ('Chingiz Aytmatov', 'Qirg\'iz va rus adabiyoti yozuvchisi', '1928-12-12'),
            ('Odil Yoqubov', 'O\'zbek yozuvchisi va jurnalist', '1934-06-05'),
            ('Pirimqul Qodirov', 'O\'zbek yozuvchisi', '1928-11-17'),
        ]

        authors = {}
        for name, bio, birth_date in authors_data:
            author, created = Author.objects.get_or_create(
                name=name,
                defaults={'bio': bio, 'birth_date': birth_date}
            )
            authors[name] = author
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created author: {name}'))

        # Create Publishers
        publishers_data = [
            ('Sharq', 'O\'zbekiston', 'https://sharq.uz'),
            ('O\'qituvchi', 'O\'zbekiston', 'https://oqituvchi.uz'),
            ('Yangi asr avlodi', 'O\'zbekiston', 'https://yangiasravlodi.uz'),
            ('G\'afur G\'ulom nomidagi', 'O\'zbekiston', ''),
        ]

        publishers = {}
        for name, country, website in publishers_data:
            publisher, created = Publisher.objects.get_or_create(
                name=name,
                defaults={'country': country, 'website': website}
            )
            publishers[name] = publisher
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created publisher: {name}'))

        # Create Books
        books_data = [
            {
                'title': 'Dunyoning ishlari',
                'author': 'O\'tkir Hoshimov',
                'genre': 'Badiy adabiyot',
                'publisher': 'Sharq',
                'isbn': '978-9943-123-45-6',
                'price': Decimal('50000'),
                'language': 'uz',
                'page_count': 350,
                'published_date': '2018-01-15',
                'description': 'O\'tkir Hoshimovning mashhur romani',
                'copies': 3
            },
            {
                'title': 'O\'tkan kunlar',
                'author': 'Abdulla Qodiriy',
                'genre': 'Badiy adabiyot',
                'publisher': 'O\'qituvchi',
                'isbn': '978-9943-123-45-7',
                'price': Decimal('45000'),
                'language': 'uz',
                'page_count': 420,
                'published_date': '2015-05-20',
                'description': 'O\'zbek adabiyotining eng yaxshi romanlaridan biri',
                'copies': 5
            },
            {
                'title': 'Mehrobdan chayon',
                'author': 'Abdulla Qodiriy',
                'genre': 'Badiy adabiyot',
                'publisher': 'O\'qituvchi',
                'isbn': '978-9943-123-45-8',
                'price': Decimal('40000'),
                'language': 'uz',
                'page_count': 380,
                'published_date': '2016-03-10',
                'description': 'Tarixiy roman',
                'copies': 4
            },
            {
                'title': 'Ufq',
                'author': 'O\'tkir Hoshimov',
                'genre': 'Badiy adabiyot',
                'publisher': 'Sharq',
                'isbn': '978-9943-123-45-9',
                'price': Decimal('55000'),
                'language': 'uz',
                'page_count': 400,
                'published_date': '2019-08-25',
                'description': 'Zamonaviy hayot haqida roman',
                'copies': 2
            },
            {
                'title': 'Yulduzli tunlar',
                'author': 'Pirimqul Qodirov',
                'genre': 'Badiy adabiyot',
                'publisher': 'G\'afur G\'ulom nomidagi',
                'isbn': '978-9943-123-46-0',
                'price': Decimal('48000'),
                'language': 'uz',
                'page_count': 360,
                'published_date': '2017-11-15',
                'description': 'Ishq va muhabbat haqida roman',
                'copies': 3
            },
            {
                'title': 'Bolalik',
                'author': 'Chingiz Aytmatov',
                'genre': 'Badiy adabiyot',
                'publisher': 'Yangi asr avlodi',
                'isbn': '978-9943-123-46-1',
                'price': Decimal('52000'),
                'language': 'uz',
                'page_count': 280,
                'published_date': '2018-06-20',
                'description': 'Bolalik xotiralari haqida',
                'copies': 4
            },
        ]

        for book_data in books_data:
            copies_count = book_data.pop('copies')
            author_name = book_data.pop('author')
            genre_name = book_data.pop('genre')
            publisher_name = book_data.pop('publisher')

            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    **book_data,
                    'slug': slugify(book_data['title']),
                    'author': authors[author_name],
                    'genre': genres[genre_name],
                    'publisher': publishers[publisher_name],
                    'is_active': True,
                    'stock_quantity': copies_count
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))

                # Create book copies
                for i in range(1, copies_count + 1):
                    copy_code = f"BK-{book.id.hex[:6].upper()}-{i:02d}"
                    BookCopy.objects.create(
                        book=book,
                        copy_code=copy_code,
                        status='good',
                        location='Asosiy ombor'
                    )
                    self.stdout.write(f'  Created copy: {copy_code}')

        self.stdout.write(self.style.SUCCESS('\nDatabase seeding completed!'))
        self.stdout.write(f'Created {Genre.objects.count()} genres')
        self.stdout.write(f'Created {Author.objects.count()} authors')
        self.stdout.write(f'Created {Publisher.objects.count()} publishers')
        self.stdout.write(f'Created {Book.objects.count()} books')
        self.stdout.write(f'Created {BookCopy.objects.count()} book copies')
