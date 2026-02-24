from pathlib import Path

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Папка с фронтендом — на уровень выше backend/
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent


def serve_index(request):
    return serve(request, 'index.html', document_root=str(FRONTEND_DIR))


urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (JWT)
    path('api/auth/', include('apps.users.urls')),

    # REST API
    path('api/events/', include('apps.events.urls')),
    path('api/submissions/', include('apps.submissions.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/notifications/', include('apps.notifications.urls')),

    # ── Фронтенд (раздача статических файлов и HTML) ──────────────────────
    # CSS и JS
    re_path(r'^css/(?P<path>.*)$', serve, {'document_root': str(FRONTEND_DIR / 'css')}),
    re_path(r'^js/(?P<path>.*)$',  serve, {'document_root': str(FRONTEND_DIR / 'js')}),

    # Страницы (pages/*.html)
    re_path(r'^pages/(?P<path>.*)$', serve, {'document_root': str(FRONTEND_DIR / 'pages')}),

    # Главная страница — / и /index.html
    path('', serve_index, name='home'),
    path('index.html', serve_index),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
