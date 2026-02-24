from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('evaluations', views.EvaluationViewSet, basename='evaluation')
router.register('results', views.EventResultViewSet, basename='result')
router.register('', views.SubmissionViewSet, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
]
