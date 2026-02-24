from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAdmin
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserListSerializer,
    UserAdminSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


# ─── Auth ─────────────────────────────────────────────────────────────────────

class LoginView(TokenObtainPairView):
    """POST /api/auth/login/ — вход, возвращает access + refresh токены."""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Обновляем last_activity после входа
        if response.status_code == 200:
            email = request.data.get('email')
            User.objects.filter(email=email).update(last_activity=timezone.now())
        return response


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — регистрация нового пользователя."""
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Генерируем токены сразу после регистрации
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserProfileSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    """POST /api/auth/logout/ — выход (инвалидация refresh-токена)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'detail': 'Выход выполнен успешно.'}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT/PATCH /api/auth/profile/ — профиль текущего пользователя."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        user = self.request.user
        user.last_activity = timezone.now()
        user.save(update_fields=['last_activity'])
        return user


class ChangePasswordView(APIView):
    """POST /api/auth/change-password/ — смена пароля."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        return Response({'detail': 'Пароль успешно изменён.'})


# ─── Users (admin) ────────────────────────────────────────────────────────────

class UserViewSet(ModelViewSet):
    """
    CRUD пользователей — только для администраторов.

    GET    /api/auth/users/          — список
    POST   /api/auth/users/          — создать
    GET    /api/auth/users/{id}/     — детали
    PUT    /api/auth/users/{id}/     — обновить
    DELETE /api/auth/users/{id}/     — удалить
    POST   /api/auth/users/{id}/block/   — заблокировать
    POST   /api/auth/users/{id}/activate/ — активировать
    """
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'status', 'institution']
    search_fields = ['email', 'first_name', 'last_name', 'institution']
    ordering_fields = ['date_joined', 'last_name', 'role']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserAdminSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password', 'changeme123')
        user = serializer.save()
        user.set_password(password)
        user.save(update_fields=['password'])

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        user = self.get_object()
        user.status = 'blocked'
        user.is_active = False
        user.save(update_fields=['status', 'is_active'])
        return Response({'detail': 'Пользователь заблокирован.'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.status = 'active'
        user.is_active = True
        user.save(update_fields=['status', 'is_active'])
        return Response({'detail': 'Пользователь активирован.'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """GET /api/auth/users/stats/ — статистика по ролям."""
        from django.db.models import Count
        stats = User.objects.values('role').annotate(count=Count('id'))
        result = {item['role']: item['count'] for item in stats}
        result['total'] = User.objects.count()
        return Response(result)
