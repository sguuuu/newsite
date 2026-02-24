from django.contrib import admin

from .models import Submission, Evaluation, EventResult


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'participant', 'event', 'status',
        'original_filename', 'submitted_at', 'jury',
    ]
    list_filter = ['status', 'event']
    search_fields = ['participant__email', 'participant__last_name', 'event__title']
    ordering = ['-submitted_at']
    readonly_fields = ['created_at', 'updated_at', 'file_size', 'original_filename']

    fieldsets = (
        (None, {'fields': ('event', 'participant', 'jury')}),
        ('Файл', {'fields': ('file', 'original_filename', 'file_size')}),
        ('Статус', {'fields': ('status', 'submitted_at')}),
        ('Мета', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['submission', 'jury', 'score', 'is_draft', 'evaluated_at']
    list_filter = ['is_draft', 'submission__event']
    search_fields = ['submission__participant__email', 'jury__email']
    readonly_fields = ['evaluated_at']


@admin.register(EventResult)
class EventResultAdmin(admin.ModelAdmin):
    list_display = ['participant', 'event', 'place', 'final_score', 'certificate_issued']
    list_filter = ['place', 'event', 'certificate_issued']
    search_fields = ['participant__email', 'participant__last_name', 'event__title']
    ordering = ['event', 'place']
