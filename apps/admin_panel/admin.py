# admin_panel/admin.py
from django.contrib import admin
from .models import StaffRole, StaffMember, ActivityLog, BlogPost, FAQ


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'can_manage_books', 'can_manage_rentals', 'can_manage_users']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'employee_id', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['user__phone', 'employee_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'created_at']
    list_filter = ['action', 'model_name', 'created_at']
    search_fields = ['user__phone', 'description', 'object_id']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'published_at', 'views_count']
    list_filter = ['status', 'published_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    ordering = ['order', '-created_at']
