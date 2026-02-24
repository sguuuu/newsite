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
