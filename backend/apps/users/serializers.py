from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT-токен с дополнительными полями пользователя."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['full_name'] = user.full_name
        token['initials'] = user.initials
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['user_id'] = self.user.id
        data['full_name'] = self.user.full_name
        data['initials'] = self.user.initials
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    consent_given = serializers.BooleanField()

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'patronymic',
            'phone', 'role', 'institution', 'grade_or_position',
            'consent_given',
        ]
        extra_kwargs = {
            'role': {'default': 'participant'},
        }

    def validate_consent_given(self, value):
        if not value:
            raise serializers.ValidationError(
                'Необходимо дать согласие на обработку персональных данных.'
            )
        return value

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError(
                {'password_confirm': 'Пароли не совпадают.'}
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['consent_given_at'] = timezone.now()
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    initials = serializers.ReadOnlyField()
    teacher_name = serializers.SerializerMethodField()
    teacher_id = serializers.PrimaryKeyRelatedField(
        source='teacher',
        queryset=User.objects.filter(role='teacher'),
        allow_null=True, required=False, write_only=False,
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'patronymic', 'phone',
            'role', 'status', 'institution', 'grade_or_position',
            'teacher_id', 'teacher_name',
            'full_name', 'initials', 'date_joined', 'last_activity',
        ]
        read_only_fields = ['id', 'role', 'status', 'date_joined', 'last_activity']

    def get_teacher_name(self, obj):
        return obj.teacher.full_name if obj.teacher else None


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    initials = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'initials', 'role', 'status',
            'institution', 'grade_or_position', 'date_joined',
        ]


class UserAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для администратора — полный доступ."""
    full_name = serializers.ReadOnlyField()
    initials = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'patronymic', 'phone',
            'role', 'status', 'institution', 'grade_or_position',
            'full_name', 'initials', 'is_active', 'date_joined', 'last_activity',
        ]
        read_only_fields = ['id', 'date_joined', 'last_activity']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Неверный текущий пароль.')
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password_confirm': 'Пароли не совпадают.'}
            )
        return data
