# books/admin.py
from django.contrib import admin
from .models import Genre, Author, Publisher, Book, BookCopy, BookReview, SimilarBook


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
    fields         = ['copy_code', 'status', 'is_available', 'barcode', 'rental_count']
    readonly_fields = ['is_available', 'rental_count']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display    = ['title', 'author', 'genre', 'language', 'rating', 'available_copies', 'is_active']
    search_fields   = ['title', 'isbn', 'author__name']
    list_filter     = ['is_active', 'genre', 'language', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'available_copies', 'rating', 'reviews_count']
    prepopulated_fields = {'slug': ('title',)}
    inlines         = [BookCopyInline]
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'isbn']
        }),
        ('Rasmlar', {
            'fields': ['cover_image', 'image_2', 'image_3', 'image_4']
        }),
        ('Muallif va janr', {
            'fields': ['author', 'genre', 'publisher']
        }),
        ('Tafsilotlar', {
            'fields': ['description', 'language', 'page_count', 'published_date', 'preview_pages']
        }),
        ('Narxlar', {
            'fields': ['price']
        }),
        ('Ijara sozlamalari', {
            'fields': ['is_active', 'max_rental_days', 'stock_quantity']
        }),
        ('Reyting', {
            'fields': ['rating', 'reviews_count']
        }),
        ('Holat', {
            'fields': ['available_copies']
        }),
        ('Tizim', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display    = ['copy_code', 'book', 'status', 'location', 'rental_count', 'is_available']
    search_fields   = ['copy_code', 'book__title', 'barcode']
    list_filter     = ['status', 'location']
    readonly_fields = ['created_at', 'updated_at', 'rental_count']


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['user__phone', 'book__title', 'review_text']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Tanlangan sharhlarni tasdiqlash"


@admin.register(SimilarBook)
class SimilarBookAdmin(admin.ModelAdmin):
    list_display = ['book', 'similar_to', 'similarity_score']
    search_fields = ['book__title', 'similar_to__title']
