from rest_framework import serializers

from apps.users.serializers import UserListSerializer
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserListSerializer(read_only=True)
    file_size_display = serializers.ReadOnlyField()
    event_title = serializers.CharField(source='event.title', read_only=True, default=None)

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'file', 'original_filename',
            'file_size', 'file_size_display', 'doc_type',
            'event', 'event_title', 'uploaded_by',
            'uploaded_at', 'download_count',
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'download_count']


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'doc_type', 'event']

    def validate_file(self, value):
        max_size = 10 * 1024 * 1024  # 10 МБ
        if value.size > max_size:
            raise serializers.ValidationError('Размер файла не должен превышать 10 МБ.')
        return value

    def create(self, validated_data):
        file = validated_data['file']
        validated_data['uploaded_by'] = self.context['request'].user
        validated_data['original_filename'] = file.name
        validated_data['file_size'] = file.size
        return super().create(validated_data)
