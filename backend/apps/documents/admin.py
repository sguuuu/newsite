from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'doc_type', 'event', 'file_size_display',
        'download_count', 'uploaded_by', 'uploaded_at',
    ]
    list_filter = ['doc_type', 'event']
    search_fields = ['title', 'description']
    ordering = ['-uploaded_at']
    readonly_fields = ['uploaded_at', 'download_count', 'file_size', 'original_filename']
