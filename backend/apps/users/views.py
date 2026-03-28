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
from .throttles import RegistrationThrottle, LoginThrottle, PasswordResetThrottle
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
    throttle_classes = [LoginThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            email = request.data.get('email')
            User.objects.filter(email=email).update(last_activity=timezone.now())
        return response


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — регистрация нового пользователя (статус pending до одобрения админом)."""
    permission_classes = [AllowAny]
    throttle_classes = [RegistrationThrottle]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()

        if new_user.role in ('teacher', 'jury'):
            # Уведомляем всех администраторов о новой заявке
            try:
                from apps.notifications.email_service import send_admin_registration_request_email
                admins = User.objects.filter(role='admin', is_active=True)
                for admin in admins:
                    send_admin_registration_request_email(admin, new_user)
            except Exception:
                pass
            return Response(
                {'detail': 'Заявка принята. Ваш аккаунт будет активирован администратором в ближайшее время.', 'needs_approval': True},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {'detail': 'Регистрация успешна! Вы можете войти в систему.', 'needs_approval': False},
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
        password = self.request.data.get('password', '').strip()
        if not password or len(password) < 8:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'password': 'Пароль обязателен и должен содержать минимум 8 символов.'})
        user = serializer.save(is_active=True, status='active')
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

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """POST /api/auth/users/{id}/approve/ — одобрить заявку на регистрацию."""
        user = self.get_object()
        if user.status != 'pending':
            return Response(
                {'detail': 'Пользователь не находится в статусе ожидания.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.status = 'active'
        user.is_active = True
        user.save(update_fields=['status', 'is_active'])
        return Response({'detail': f'Пользователь {user.full_name} одобрен.'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """GET /api/auth/users/stats/ — статистика по ролям."""
        from django.db.models import Count
        stats = User.objects.values('role').annotate(count=Count('id'))
        result = {item['role']: item['count'] for item in stats}
        result['total'] = User.objects.count()
        result['pending'] = User.objects.filter(status='pending').count()
        return Response(result)

    @action(detail=True, methods=['post'])
    def assign_teacher(self, request, pk=None):
        """POST /api/auth/users/{id}/assign_teacher/ — назначить педагога участнику (admin)."""
        user = self.get_object()
        teacher_id = request.data.get('teacher_id')
        if teacher_id:
            try:
                teacher = User.objects.get(id=teacher_id, role='teacher')
                user.teacher = teacher
            except User.DoesNotExist:
                return Response({'detail': 'Педагог не найден.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user.teacher = None
        user.save(update_fields=['teacher'])
        return Response(UserListSerializer(user).data)


# ─── Teachers list (public for participants) ──────────────────────────────────

class TeacherListView(generics.ListAPIView):
    """GET /api/auth/teachers/ — список активных педагогов (для выбора участником)."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.filter(role='teacher', status='active').order_by('last_name')


# ─── Teacher: my students ─────────────────────────────────────────────────────

class MyStudentsView(APIView):
    """
    GET  /api/auth/my-students/        — список учеников с прогрессом
    POST /api/auth/my-students/add/    — добавить ученика по email
    DELETE /api/auth/my-students/{id}/ — отвязать ученика
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'teacher':
            return Response(status=status.HTTP_403_FORBIDDEN)

        from apps.submissions.models import Submission, EventResult
        students = request.user.students.filter(status='active').order_by('last_name')

        result = []
        for s in students:
            submissions = Submission.objects.filter(participant=s)
            results = EventResult.objects.filter(participant=s, place__gt=0, place__lte=3)
            from apps.events.models import EventRegistration
            events = EventRegistration.objects.filter(
                participant=s, status__in=('registered', 'active', 'completed')
            ).select_related('event')

            result.append({
                'id': s.id,
                'full_name': s.full_name,
                'email': s.email,
                'institution': s.institution,
                'grade_or_position': s.grade_or_position,
                'initials': s.initials,
                'events': [
                    {
                        'id': r.event.id,
                        'title': r.event.title,
                        'status': r.event.status,
                        'reg_status': r.status,
                    }
                    for r in events
                ],
                'submissions': [
                    {
                        'id': sub.id,
                        'event_title': sub.event.title,
                        'status': sub.status,
                        'score': sub.evaluation.score if hasattr(sub, 'evaluation') else None,
                        'submitted_at': sub.submitted_at,
                    }
                    for sub in submissions.select_related('event')
                ],
                'prizes': results.count(),
            })

        return Response(result)


class TeacherRequestView(APIView):
    """
    Заявки на прикрепление к педагогу.

    Участник:
      GET  /api/auth/teacher-requests/           — свои заявки
      POST /api/auth/teacher-requests/           — отправить заявку педагогу
      DELETE /api/auth/teacher-requests/{id}/    — отозвать заявку

    Педагог:
      GET  /api/auth/teacher-requests/           — входящие заявки
      POST /api/auth/teacher-requests/{id}/approve/ — принять
      POST /api/auth/teacher-requests/{id}/reject/  — отклонить
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .models import TeacherRequest
        user = request.user
        if user.role == 'participant':
            qs = TeacherRequest.objects.filter(participant=user).select_related('teacher')
            data = [
                {
                    'id': r.id,
                    'teacher_id': r.teacher.id,
                    'teacher_name': r.teacher.full_name,
                    'teacher_institution': r.teacher.institution,
                    'status': r.status,
                    'message': r.message,
                    'created_at': r.created_at,
                }
                for r in qs
            ]
        elif user.role == 'teacher':
            qs = TeacherRequest.objects.filter(
                teacher=user, status='pending'
            ).select_related('participant')
            # Возвращаем только ФИО и учреждение — БЕЗ email
            data = [
                {
                    'id': r.id,
                    'participant_id': r.participant.id,
                    'participant_name': r.participant.full_name,
                    'participant_institution': r.participant.institution,
                    'participant_grade': r.participant.grade_or_position,
                    'message': r.message,
                    'created_at': r.created_at,
                }
                for r in qs
            ]
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(data)

    def post(self, request):
        from .models import TeacherRequest
        user = request.user
        if user.role != 'participant':
            return Response(
                {'detail': 'Только участники могут отправлять заявки.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        teacher_id = request.data.get('teacher_id')
        message = request.data.get('message', '').strip()
        if not teacher_id:
            return Response({'detail': 'Укажите teacher_id.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            teacher = User.objects.get(id=teacher_id, role='teacher', status='active')
        except User.DoesNotExist:
            return Response({'detail': 'Педагог не найден.'}, status=status.HTTP_404_NOT_FOUND)
        if user.teacher:
            return Response(
                {'detail': 'Вы уже прикреплены к педагогу. Сначала отвяжитесь от текущего педагога.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        req, created = TeacherRequest.objects.get_or_create(
            participant=user, teacher=teacher,
            defaults={'message': message, 'status': 'pending'},
        )
        if not created:
            if req.status == 'pending':
                return Response({'detail': 'Заявка уже отправлена и ожидает ответа.'}, status=status.HTTP_400_BAD_REQUEST)
            # Повторная заявка после отклонения
            req.status = 'pending'
            req.message = message
            req.responded_at = None
            req.save(update_fields=['status', 'message', 'responded_at'])
        return Response({'detail': f'Заявка отправлена педагогу {teacher.full_name}.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        from .models import TeacherRequest
        if request.user.role != 'participant':
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            req = TeacherRequest.objects.get(id=pk, participant=request.user, status='pending')
        except TeacherRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        req.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherRequestActionView(APIView):
    """POST /api/auth/teacher-requests/{id}/approve|reject/"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, action):
        from .models import TeacherRequest
        if request.user.role != 'teacher':
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            req = TeacherRequest.objects.get(id=pk, teacher=request.user, status='pending')
        except TeacherRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if action == 'approve':
            req.status = 'approved'
            req.responded_at = timezone.now()
            req.save(update_fields=['status', 'responded_at'])
            req.participant.teacher = request.user
            req.participant.save(update_fields=['teacher'])
            return Response({'detail': f'{req.participant.full_name} прикреплён к вам.'})
        elif action == 'reject':
            req.status = 'rejected'
            req.responded_at = timezone.now()
            req.save(update_fields=['status', 'responded_at'])
            return Response({'detail': 'Заявка отклонена.'})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RemoveStudentView(APIView):
    """DELETE /api/auth/my-students/<id>/remove/ — педагог отвязывает ученика."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if request.user.role != 'teacher':
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            student = User.objects.get(id=pk, teacher=request.user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        student.teacher = None
        student.save(update_fields=['teacher'])
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Password Reset ────────────────────────────────────────────────────────────

class PasswordResetRequestView(APIView):
    """
    POST /api/auth/password-reset/
    Тело: { "email": "user@example.com" }
    Всегда возвращает 200 (не раскрываем факт существования email).
    """
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetThrottle]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        if not email:
            return Response({'detail': 'Укажите email.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, is_active=True)
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.encoding import force_bytes
            from django.utils.http import urlsafe_base64_encode
            from django.conf import settings
            from apps.notifications.email_service import send_password_reset_email

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_URL}/auth/reset-password?uid={uid}&token={token}"
            send_password_reset_email(user, reset_link)
        except User.DoesNotExist:
            pass  # Молча игнорируем — не раскрываем наличие email

        return Response({'detail': 'Если такой email зарегистрирован, письмо отправлено.'})


class PasswordResetConfirmView(APIView):
    """
    POST /api/auth/password-reset/confirm/
    Тело: { "uid": "...", "token": "...", "new_password": "..." }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid', '')
        token = request.data.get('token', '')
        new_password = request.data.get('new_password', '')

        if not all([uid, token, new_password]):
            return Response(
                {'detail': 'Необходимы uid, token и new_password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(new_password) < 8:
            return Response(
                {'detail': 'Пароль должен содержать минимум 8 символов.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode

        try:
            pk = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=pk)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'detail': 'Ссылка недействительна.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response(
                {'detail': 'Ссылка устарела или уже использована. Запросите новую.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=['password'])
        return Response({'detail': 'Пароль успешно изменён. Войдите с новым паролем.'})
