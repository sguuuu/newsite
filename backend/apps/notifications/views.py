from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Уведомления текущего пользователя.

    GET  /api/notifications/              — список уведомлений
    GET  /api/notifications/{id}/         — одно уведомление
    POST /api/notifications/{id}/read/    — отметить как прочитанное
    POST /api/notifications/read-all/     — прочитать все
    GET  /api/notifications/unread-count/ — количество непрочитанных
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({'detail': 'Отмечено как прочитанное.'})

    @action(detail=False, methods=['post'])
    def read_all(self, request):
        count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'detail': f'Прочитано {count} уведомлений.'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread': count})

    @action(detail=False, methods=['post'])
    def check_deadlines(self, request):
        """
        POST /api/notifications/check-deadlines/
        Создаёт уведомления о приближающихся дедлайнах для текущего пользователя.
        Вызывается с фронтенда при входе и периодически.
        """
        from django.utils import timezone
        from datetime import timedelta
        from apps.events.models import EventRegistration

        user = request.user
        if user.role != 'participant':
            return Response({'created': 0})

        today = timezone.now().date()
        created = 0

        # Регистрации на активные/предстоящие мероприятия с дедлайном
        registrations = EventRegistration.objects.filter(
            participant=user,
            status__in=['registered', 'active'],
            event__status__in=['active', 'upcoming'],
            event__registration_deadline__isnull=False,
        ).select_related('event')

        for reg in registrations:
            deadline = reg.event.registration_deadline
            if hasattr(deadline, 'date'):
                deadline_date = deadline.date()
            else:
                deadline_date = deadline

            days_left = (deadline_date - today).days

            if days_left not in (7, 3, 1):
                continue

            # Не создавать дубли — проверяем по заголовку и получателю
            title = f'Дедлайн через {days_left} дн.: «{reg.event.title}»'
            already_exists = Notification.objects.filter(
                recipient=user,
                notif_type='deadline',
                title=title,
            ).exists()
            if already_exists:
                continue

            Notification.objects.create(
                recipient=user,
                title=title,
                message=f'До окончания приёма работ по «{reg.event.title}» осталось {days_left} дн. Не забудьте загрузить работу.',
                notif_type='deadline',
            )
            created += 1

        return Response({'created': created})
