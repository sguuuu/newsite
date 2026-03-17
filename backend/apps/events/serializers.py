from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.serializers import UserListSerializer
from .models import Event, EventRegistration, JuryAssignment

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


class EventRegistrationSerializer(serializers.ModelSerializer):
    participant = UserListSerializer(read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_type = serializers.CharField(source='event.event_type', read_only=True)

    class Meta:
        model = EventRegistration
        fields = [
            'id', 'event', 'event_title', 'event_type',
            'participant', 'status', 'registered_at', 'completion_percentage',
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

    class Meta:
        model = JuryAssignment
        fields = ['id', 'jury', 'jury_id', 'event', 'event_title', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']
