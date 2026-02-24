from django.http import FileResponse
from rest_framework import generics, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.permissions import IsAdmin
from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer


class DocumentViewSet(ModelViewSet):
    """
    Документы платформы.

    GET    /api/documents/          — список (публично)
    POST   /api/documents/          — загрузить (admin)
    GET    /api/documents/{id}/     — детали (публично)
    DELETE /api/documents/{id}/     — удалить (admin)
    GET    /api/documents/{id}/download/ — скачать файл
    """
    queryset = Document.objects.select_related('uploaded_by', 'event').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['doc_type', 'event']
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'title', 'download_count']
    ordering = ['-uploaded_at']

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'download'):
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentUploadSerializer
        return DocumentSerializer

    def perform_destroy(self, instance):
        instance.file.delete(save=False)
        instance.delete()

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """GET /api/documents/{id}/download/ — скачать файл, увеличивает счётчик."""
        document = self.get_object()
        try:
            response = FileResponse(
                document.file.open('rb'),
                as_attachment=True,
                filename=document.original_filename,
            )
            document.download_count += 1
            document.save(update_fields=['download_count'])
            return response
        except FileNotFoundError:
            return Response(
                {'detail': 'Файл не найден на сервере.'},
                status=status.HTTP_404_NOT_FOUND,
            )
