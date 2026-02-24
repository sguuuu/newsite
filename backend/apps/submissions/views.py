from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.permissions import IsAdmin, IsJury, IsParticipant
from .models import Submission, Evaluation, EventResult
from .serializers import (
    SubmissionSerializer,
    SubmissionUploadSerializer,
    EvaluationSerializer,
    EventResultSerializer,
)


class SubmissionViewSet(ModelViewSet):
    """
    Работы участников.

    GET    /api/submissions/         — список (свои или назначенные жюри)
    POST   /api/submissions/         — загрузить работу (participant)
    GET    /api/submissions/{id}/    — детали
    DELETE /api/submissions/{id}/    — удалить (admin или сам участник до сабмита)
    POST   /api/submissions/{id}/submit/    — подать работу официально
    POST   /api/submissions/{id}/assign_jury/ — назначить жюри (admin)
    """
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'event']
    ordering_fields = ['submitted_at', 'created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [IsParticipant()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return SubmissionUploadSerializer
        return SubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Submission.objects.select_related('event', 'participant', 'jury').all()
        if user.role == 'jury':
            return Submission.objects.filter(jury=user).select_related('event', 'participant')
        if user.role == 'teacher':
            return Submission.objects.filter(
                participant__teacher=user
            ).select_related('event', 'participant')
        # participant
        return Submission.objects.filter(participant=user).select_related('event')

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role != 'admin' and (
            instance.participant != user or instance.status != 'draft'
        ):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Нельзя удалить поданную работу.')
        instance.file.delete(save=False)
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsParticipant])
    def submit(self, request, pk=None):
        submission = self.get_object()
        if submission.participant != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if submission.status != 'draft':
            return Response(
                {'detail': 'Работа уже подана.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        submission.status = 'submitted'
        submission.submitted_at = timezone.now()
        submission.save(update_fields=['status', 'submitted_at'])

        from apps.notifications.models import Notification
        Notification.objects.create(
            recipient=request.user,
            title='Работа подана',
            message=f'Ваша работа на "{submission.event.title}" успешно отправлена на проверку.',
            notif_type='submission',
        )
        return Response(SubmissionSerializer(submission).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def assign_jury(self, request, pk=None):
        submission = self.get_object()
        jury_id = request.data.get('jury_id')
        if not jury_id:
            return Response(
                {'detail': 'Необходимо указать jury_id.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            jury = User.objects.get(id=jury_id, role='jury')
        except User.DoesNotExist:
            return Response(
                {'detail': 'Жюри не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        submission.jury = jury
        submission.status = 'under_review'
        submission.save(update_fields=['jury', 'status'])
        return Response(SubmissionSerializer(submission).data)


# ─── Evaluations ──────────────────────────────────────────────────────────────

class EvaluationViewSet(ModelViewSet):
    """
    Оценки работ.

    GET    /api/submissions/evaluations/         — список
    POST   /api/submissions/evaluations/         — создать оценку (jury)
    PUT    /api/submissions/evaluations/{id}/    — обновить (jury, пока черновик)
    """
    serializer_class = EvaluationSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update'):
            return [IsJury()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Evaluation.objects.select_related('submission', 'jury').all()
        if user.role == 'jury':
            return Evaluation.objects.filter(jury=user).select_related('submission')
        # participant — видит оценки своих работ
        return Evaluation.objects.filter(
            submission__participant=user
        ).select_related('submission')

    def perform_update(self, serializer):
        instance = self.get_object()
        if not instance.is_draft:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Финальная оценка не может быть изменена.')
        serializer.save()

    def perform_create(self, serializer):
        evaluation = serializer.save()
        # Если не черновик — обновляем статус работы
        if not evaluation.is_draft:
            self._finalize_evaluation(evaluation)

    def _finalize_evaluation(self, evaluation):
        submission = evaluation.submission
        submission.status = 'evaluated'
        submission.save(update_fields=['status'])

        from apps.notifications.models import Notification
        Notification.objects.create(
            recipient=submission.participant,
            title='Ваша работа проверена',
            message=(
                f'Жюри оценил вашу работу по "{submission.event.title}". '
                f'Балл: {evaluation.score}/100.'
            ),
            notif_type='evaluation',
        )

    @action(detail=True, methods=['post'], permission_classes=[IsJury])
    def finalize(self, request, pk=None):
        """POST /api/submissions/evaluations/{id}/finalize/ — опубликовать оценку."""
        evaluation = self.get_object()
        if evaluation.jury != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not evaluation.is_draft:
            return Response({'detail': 'Оценка уже финализирована.'})
        evaluation.is_draft = False
        evaluation.save(update_fields=['is_draft'])
        self._finalize_evaluation(evaluation)
        return Response(EvaluationSerializer(evaluation).data)


# ─── Results ──────────────────────────────────────────────────────────────────

class EventResultViewSet(ModelViewSet):
    """
    Итоговые результаты мероприятий.
    """
    serializer_class = EventResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'place']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return EventResult.objects.select_related('event', 'participant').all()
        return EventResult.objects.filter(
            participant=user
        ).select_related('event', 'submission')
