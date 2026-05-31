# books/serializers.py
from rest_framework import serializers
from .models import Book, Author, Genre, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Author
        fields = ['id', 'name', 'bio']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Genre
        fields = ['id', 'name', 'slug']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Publisher
        fields = ['id', 'name', 'country', 'website']


class BookListSerializer(serializers.ModelSerializer):
    authors          = AuthorSerializer(many=True, read_only=True)
    genres           = GenreSerializer(many=True, read_only=True)
    available_copies = serializers.SerializerMethodField()

    def get_available_copies(self, obj):
        if hasattr(obj, 'available_copies_list'):
            return len(obj.available_copies_list)
        return obj.copies.exclude(status__in=['lost', 'poor']).exclude(rentals__status='active').count()

    class Meta:
        model  = Book
        fields = [
            'id', 'title', 'slug', 'authors', 'genres',
            'language', 'rental_price_daily', 'deposit_amount',
            'cover_image', 'available_copies'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    authors          = AuthorSerializer(many=True, read_only=True)
    genres           = GenreSerializer(many=True, read_only=True)
    publisher        = PublisherSerializer(read_only=True)
    available_copies = serializers.SerializerMethodField()

    def get_available_copies(self, obj):
        if hasattr(obj, 'available_copies_list'):
            return len(obj.available_copies_list)
        return obj.copies.exclude(status__in=['lost', 'poor']).exclude(rentals__status='active').count()

    class Meta:
        model  = Book
        fields = [
            'id', 'title', 'slug', 'isbn',
            'authors', 'genres', 'publisher',
            'description', 'language', 'page_count', 'published_year',
            'rental_price_daily', 'rental_price_weekly', 'rental_price_monthly',
            'deposit_amount', 'cover_image', 'preview_pages',
            'available_copies', 'is_active'
        ]