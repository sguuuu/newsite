from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('jury-assignments', views.JuryAssignmentViewSet, basename='jury-assignment')
router.register('stages', views.EventStageViewSet, basename='stage')
router.register('tasks', views.EventTaskViewSet, basename='task')
router.register('reg-docs', views.RegistrationDocumentViewSet, basename='reg-doc')
router.register('', views.EventViewSet, basename='event')

urlpatterns = [
    path('my-registrations/', views.MyRegistrationsView.as_view(), name='my-registrations'),
    path('dashboard-stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('', include(router.urls)),
]
