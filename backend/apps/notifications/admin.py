from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notif_type', 'is_read', 'created_at']
    list_filter = ['notif_type', 'is_read']
    search_fields = ['title', 'message', 'recipient__email']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

    actions = ['mark_as_read']

    @admin.action(description='Отметить как прочитанные')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
