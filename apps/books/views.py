# books/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from .models import Book, BookCopy
from .serializers import BookListSerializer, BookDetailSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filter
    filterset_fields = ['genre__slug', 'author__id']

    # Search
    search_fields = ['title', 'author__name', 'isbn']

    # Ordering
    ordering_fields  = ['title', 'price', 'published_date']
    ordering         = ['-created_at']  # default

    def get_queryset(self):
        return (
            Book.objects
            .select_related('publisher', 'author', 'genre')
            .prefetch_related(
                Prefetch(
                    'copies',
                    queryset=BookCopy.objects.exclude(
                        status__in=['lost', 'poor']
                    ).exclude(
                        rentals__status__in=['pending', 'active', 'overdue']
                    ),
                    to_attr='available_copies_list'             # N+1 fix
                )
            )
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookListSerializer


# books/views.py ga qo'shiladi

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import BookCopy
from apps.copies.serializers import BookCopySerializer, BookCopyCreateSerializer


class BookCopyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['status', 'book__id']
    search_fields      = ['copy_code', 'book__title']
    ordering_fields    = ['created_at']
    ordering           = ['-created_at']

    def get_queryset(self):
        return (
            BookCopy.objects
            .select_related('book__publisher', 'book__author')
            .filter(book__is_active=True)
        )

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookCopyCreateSerializer
        return BookCopySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
