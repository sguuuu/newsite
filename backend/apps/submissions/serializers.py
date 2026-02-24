from rest_framework import serializers

from apps.users.serializers import UserListSerializer
from apps.events.serializers import EventListSerializer
from .models import Submission, Evaluation, EventResult


class SubmissionSerializer(serializers.ModelSerializer):
    participant = UserListSerializer(read_only=True)
    jury = UserListSerializer(read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    file_size_kb = serializers.SerializerMethodField()
    has_evaluation = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            'id', 'event', 'event_title', 'participant', 'jury',
            'file', 'original_filename', 'file_size', 'file_size_kb',
            'status', 'submitted_at', 'has_evaluation',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'participant', 'created_at', 'updated_at']

    def get_file_size_kb(self, obj):
        return round(obj.file_size / 1024, 1)

    def get_has_evaluation(self, obj):
        return hasattr(obj, 'evaluation')


class SubmissionUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['event', 'file']

    def validate_file(self, value):
        max_size = 20 * 1024 * 1024  # 20 МБ
        if value.size > max_size:
            raise serializers.ValidationError('Размер файла не должен превышать 20 МБ.')
        allowed = ['.pdf', '.doc', '.docx', '.zip', '.rar']
        ext = '.' + value.name.split('.')[-1].lower()
        if ext not in allowed:
            raise serializers.ValidationError(
                f'Разрешённые форматы: {", ".join(allowed)}.'
            )
        return value

    def create(self, validated_data):
        file = validated_data['file']
        validated_data['participant'] = self.context['request'].user
        validated_data['original_filename'] = file.name
        validated_data['file_size'] = file.size
        return super().create(validated_data)


class EvaluationSerializer(serializers.ModelSerializer):
    jury = UserListSerializer(read_only=True)

    class Meta:
        model = Evaluation
        fields = [
            'id', 'submission', 'jury',
            'score', 'feedback',
            'criteria_completeness', 'criteria_accuracy',
            'criteria_examples', 'criteria_grammar',
            'is_draft', 'evaluated_at',
        ]
        read_only_fields = ['id', 'jury', 'evaluated_at']

    def create(self, validated_data):
        validated_data['jury'] = self.context['request'].user
        return super().create(validated_data)


class EventResultSerializer(serializers.ModelSerializer):
    participant = UserListSerializer(read_only=True)
    event = EventListSerializer(read_only=True)

    class Meta:
        model = EventResult
        fields = [
            'id', 'event', 'participant', 'submission',
            'place', 'final_score', 'certificate_issued', 'published_at',
        ]
        read_only_fields = ['id', 'published_at']
