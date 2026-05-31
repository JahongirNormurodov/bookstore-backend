from rest_framework import serializers
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'passport_number',
            'birth_date',
            'address',
            'is_phone_verified',
            'is_passport_verified',
        ]
        read_only_fields = ['is_phone_verified', 'is_passport_verified']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    trust_score = serializers.IntegerField(source='current_trust_score', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'phone',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'profile',
            'trust_score',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['phone', 'email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


# users/serializers.py

import re
from django.utils.timezone import now
from rest_framework import serializers
from .models import OTPCode


class SendOTPSerializer(serializers.Serializer):
    """Telefonga SMS kod yuborish"""

    phone = serializers.CharField(max_length=15)

    def validate_phone(self, value):
        value = value.strip()

        # Format: +998XXXXXXXXX
        pattern = r'^\+998[0-9]{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Telefon raqam formati noto'g'ri. Namuna: +998901234567"
            )
        return value


class VerifyOTPSerializer(serializers.Serializer):
    """SMS kodini tasdiqlash"""

    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)
    purpose = serializers.ChoiceField(choices=OTPCode.Purpose.choices)

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')
        purpose = attrs.get('purpose')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError({"phone": "Ushbu telefon raqamli foydalanuvchi topilmadi."})

        otp = OTPCode.objects.filter(
            user=user,
            code=code,
            purpose=purpose
        ).first()

        if not otp:
            raise serializers.ValidationError({"code": "Tasdiqlash kodi noto'g'ri."})

        if not otp.is_valid:
            raise serializers.ValidationError({"code": "Tasdiqlash kodi muddati o'tgan yoki allaqachon ishlatilgan."})

        attrs['user'] = user
        attrs['otp'] = otp
        return attrs


