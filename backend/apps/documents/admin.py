from django.contrib import admin
from django.contrib.auth import get_user_model

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

    def save_model(self, request, obj, form, change):
        if obj.file:
            obj.original_filename = obj.file.name.split('/')[-1].split('\\')[-1]
            obj.file_size = obj.file.size
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
