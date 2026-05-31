# books/admin.py
from django.contrib import admin
from .models import Genre, Author, Publisher, Book, BookCopy


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display       = ['name', 'slug', 'created_at']
    search_fields      = ['name']
    prepopulated_fields = {'slug': ('name',)}  # name yozilganda slug avtomatik
    readonly_fields    = ['created_at', 'updated_at']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display    = ['name', 'birth_date', 'created_at']
    search_fields   = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        (None, {
            'fields': ['name', 'photo', 'birth_date']
        }),
        ('Qo\'shimcha', {
            'fields': ['bio'],
            'classes': ['collapse']   # admin da yig'ilib turadi
        }),
        ('Tizim', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display    = ['name', 'country', 'website', 'created_at']
    search_fields   = ['name', 'country']
    readonly_fields = ['created_at', 'updated_at']


class BookCopyInline(admin.TabularInline):
    # Book admin ichida nusxalarni ko'rsatish
    model          = BookCopy
    extra          = 0
    fields         = ['copy_code', 'status', 'is_available']
    readonly_fields = ['is_available']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display    = ['title', 'published_year', 'language', 'available_copies', 'is_active']
    search_fields   = ['title', 'isbn', 'authors__name']
    list_filter     = ['genre', 'publisher']
    readonly_fields = ['created_at', 'updated_at', 'available_copies']
    prepopulated_fields = {'slug': ('title',)}
    inlines         = [BookCopyInline]
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'isbn', 'cover_image']
        }),
        ('Muallif va janr', {
            'fields': ['authors', 'genres', 'publisher']
        }),
        ('Tafsilotlar', {
            'fields': ['description', 'language', 'page_count', 'published_year']
        }),
        ('Narxlar', {
            'fields': ['rental_price_daily', 'rental_price_weekly',
                       'rental_price_monthly', 'deposit_amount']
        }),
        ('Holat', {
            'fields': ['is_active', 'available_copies', 'total_copies']
        }),
        ('Tizim', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display    = ['copy_code', 'book', 'status', 'is_available']
    search_fields   = ['copy_code', 'book__title']
    list_filter     = ['status']
    readonly_fields = ['created_at', 'updated_at']
