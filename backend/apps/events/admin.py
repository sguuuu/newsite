from django.contrib import admin

from .models import Event, EventRegistration, JuryAssignment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'event_type', 'status', 'format',
        'start_date', 'end_date', 'registration_deadline',
        'participant_count', 'is_registration_open',
    ]
    list_filter = ['event_type', 'status', 'format']
    search_fields = ['title', 'description']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'

    fieldsets = (
        (None, {'fields': ('title', 'description', 'short_description')}),
        ('Тип и статус', {'fields': ('event_type', 'status', 'format')}),
        ('Даты', {'fields': ('start_date', 'end_date', 'registration_deadline')}),
        ('Ограничения', {'fields': ('max_participants', 'age_min', 'age_max')}),
        ('Мета', {'fields': ('created_by', 'created_at', 'updated_at')}),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['participant', 'event', 'status', 'registered_at', 'completion_percentage']
    list_filter = ['status', 'event']
    search_fields = ['participant__email', 'participant__last_name', 'event__title']
    ordering = ['-registered_at']
    readonly_fields = ['registered_at']


@admin.register(JuryAssignment)
class JuryAssignmentAdmin(admin.ModelAdmin):
    list_display = ['jury', 'event', 'assigned_at']
    list_filter = ['event']
    search_fields = ['jury__email', 'event__title']
    readonly_fields = ['assigned_at']
