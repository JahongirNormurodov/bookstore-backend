from django.contrib import admin
from .models import User, Profile, TrustScore, OTPCode, Wishlist, SearchHistory, ReferralCode, Referral, LoyaltyPoints


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'first_name', 'last_name', 'is_active', 'current_trust_score', 'total_loyalty_points']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['phone', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login', 'current_trust_score', 'total_loyalty_points']
    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'passport_number', 'is_phone_verified', 'is_passport_verified', 'is_blacklisted']
    list_filter = ['is_phone_verified', 'is_passport_verified', 'is_blacklisted']
    search_fields = ['user__phone', 'passport_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TrustScore)
class TrustScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'reason', 'changed_by', 'created_at']
    list_filter = ['reason', 'created_at']
    search_fields = ['user__phone', 'comment']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'purpose', 'is_used', 'is_expired', 'created_at']
    list_filter = ['purpose', 'is_used', 'created_at']
    search_fields = ['user__phone', 'code']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at']
    search_fields = ['user__phone', 'book__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'results_count', 'created_at']
    search_fields = ['user__phone', 'query']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'uses_count', 'created_at']
    search_fields = ['user__phone', 'code']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred', 'reward_given', 'created_at']
    list_filter = ['reward_given']
    search_fields = ['referrer__phone', 'referred__phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'reason', 'created_at']
    list_filter = ['reason', 'created_at']
    search_fields = ['user__phone', 'description']
    readonly_fields = ['created_at', 'updated_at']
