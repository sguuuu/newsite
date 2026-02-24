from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'full_name', 'role', 'status',
        'institution', 'date_joined', 'is_active',
    ]
    list_filter = ['role', 'status', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name', 'institution']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_activity']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name', 'patronymic', 'phone')}),
        ('Роль и статус', {'fields': ('role', 'status')}),
        ('Учреждение', {'fields': ('institution', 'grade_or_position', 'teacher')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('date_joined', 'last_activity')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'first_name', 'last_name', 'role',
            ),
        }),
    )
