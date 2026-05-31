from rest_framework import serializers
from apps.books.models import BookCopy
from apps.books.serializers import BookListSerializer

class BookCopySerializer(serializers.ModelSerializer):
    """Kitob nusxasini ko'rish uchun"""
    book         = BookListSerializer(read_only=True)
    book_id      = serializers.UUIDField(write_only=True)  # create uchun
    status_label = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model  = BookCopy
        fields = [
            'id', 'book', 'book_id',
            'copy_code',
            'status', 'status_label',
            'is_available',
        ]
        read_only_fields = ['id', 'is_available']


class BookCopyCreateSerializer(serializers.ModelSerializer):
    """Admin kitob nusxasi qo'shishi uchun"""

    class Meta:
        model  = BookCopy
        fields = ['book', 'copy_code', 'status']

    def validate_copy_code(self, value):
        if BookCopy.objects.filter(copy_code=value).exists():
            raise serializers.ValidationError(
                "Bu nusxa kodi allaqachon mavjud."
            )
        return value