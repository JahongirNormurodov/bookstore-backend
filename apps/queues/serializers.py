# queues/serializers.py
from rest_framework import serializers
from .models import BookQueue, BookNotification
from apps.books.serializers import BookListSerializer


class BookQueueSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    book_details = BookListSerializer(source='book', read_only=True)
    
    class Meta:
        model = BookQueue
        fields = [
            'id', 'user', 'user_phone', 'book', 'book_details',
            'status', 'position', 'notified_at', 'expires_at',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'position', 'created_at', 'updated_at']


class BookQueueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookQueue
        fields = ['book']
    
    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data['book']
        
        # Check if already in queue
        existing = BookQueue.objects.filter(
            user=user, 
            book=book, 
            status='waiting'
        ).first()
        
        if existing:
            raise serializers.ValidationError("You are already in the queue for this book")
        
        # Get next position
        last_position = BookQueue.objects.filter(
            book=book, 
            status='waiting'
        ).order_by('-position').first()
        
        position = (last_position.position + 1) if last_position else 1
        
        return BookQueue.objects.create(
            user=user,
            book=book,
            position=position,
            **validated_data
        )


class BookNotificationSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_cover = serializers.ImageField(source='book.cover_image', read_only=True)
    
    class Meta:
        model = BookNotification
        fields = [
            'id', 'user', 'user_phone', 'book', 'book_title', 'book_cover',
            'is_notified', 'notified_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_notified', 'notified_at', 'created_at', 'updated_at']


class BookNotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNotification
        fields = ['book']
    
    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data['book']
        
        # Check if already subscribed
        existing = BookNotification.objects.filter(
            user=user,
            book=book,
            is_notified=False
        ).first()
        
        if existing:
            raise serializers.ValidationError("You are already subscribed to notifications for this book")
        
        return BookNotification.objects.create(user=user, **validated_data)
