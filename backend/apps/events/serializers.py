from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.serializers import UserListSerializer
from .models import Event, EventRegistration, JuryAssignment, EventStage, EventTask, RegistrationDocument

User = get_user_model()


class EventListSerializer(serializers.ModelSerializer):
    participant_count = serializers.ReadOnlyField()
    is_registration_open = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'short_description', 'event_type', 'movement_type',
            'status', 'format',
            'start_date', 'end_date', 'registration_deadline',
            'participant_count', 'is_registration_open', 'max_participants',
            'requires_parental_consent', 'requires_application', 'sequential_stages',
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    participant_count = serializers.ReadOnlyField()
    is_registration_open = serializers.ReadOnlyField()
    created_by = UserListSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'short_description',
            'event_type', 'movement_type', 'status', 'format',
            'start_date', 'end_date', 'registration_deadline',
            'max_participants', 'age_min', 'age_max',
            'requires_parental_consent', 'requires_application', 'sequential_stages',
        ]

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        deadline = data.get('registration_deadline')
        if start and end and start > end:
            raise serializers.ValidationError(
                'Дата начала не может быть позже даты окончания.'
            )
        if deadline and start and deadline > start:
            raise serializers.ValidationError(
                'Дедлайн регистрации должен быть до начала мероприятия.'
            )
        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class RegistrationDocumentSerializer(serializers.ModelSerializer):
    reviewed_by_name = serializers.CharField(source='reviewed_by.full_name', read_only=True)

    class Meta:
        model = RegistrationDocument
        fields = [
            'id', 'registration', 'doc_type', 'file',
            'parent_full_name', 'parent_phone', 'comment',
            'status', 'admin_note', 'submitted_at', 'reviewed_at', 'reviewed_by_name',
        ]
        read_only_fields = ['id', 'status', 'admin_note', 'submitted_at', 'reviewed_at', 'reviewed_by_name']

    def validate_file(self, value):
        if value and value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('Размер файла не должен превышать 10 МБ.')
        return value


class EventRegistrationSerializer(serializers.ModelSerializer):
    participant = UserListSerializer(read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_type = serializers.CharField(source='event.event_type', read_only=True)
    documents = RegistrationDocumentSerializer(many=True, read_only=True)
    requires_parental_consent = serializers.BooleanField(source='event.requires_parental_consent', read_only=True)
    requires_application = serializers.BooleanField(source='event.requires_application', read_only=True)

    class Meta:
        model = EventRegistration
        fields = [
            'id', 'event', 'event_title', 'event_type',
            'participant', 'status', 'registered_at', 'completion_percentage',
            'documents', 'requires_parental_consent', 'requires_application',
        ]
        read_only_fields = ['id', 'registered_at']


class JuryAssignmentSerializer(serializers.ModelSerializer):
    jury = UserListSerializer(read_only=True)
    jury_id = serializers.PrimaryKeyRelatedField(
        source='jury',
        queryset=User.objects.filter(role='jury'),
        write_only=True,
    )
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_status = serializers.CharField(source='event.status', read_only=True)

    class Meta:
        model = JuryAssignment
        fields = ['id', 'jury', 'jury_id', 'event', 'event_title', 'event_status', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']


class EventTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTask
        fields = ['id', 'stage', 'title', 'description', 'order', 'max_score', 'file']
        read_only_fields = ['id']

    def validate_file(self, value):
        if value and value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('Размер файла не должен превышать 10 МБ.')
        return value


class EventStageSerializer(serializers.ModelSerializer):
    tasks = EventTaskSerializer(many=True, read_only=True)

    class Meta:
        model = EventStage
        fields = ['id', 'event', 'title', 'description', 'order', 'start_date', 'end_date', 'tasks']
        read_only_fields = ['id']
