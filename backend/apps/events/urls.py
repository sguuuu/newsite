from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('', views.EventViewSet, basename='event')
router.register('jury-assignments', views.JuryAssignmentViewSet, basename='jury-assignment')

urlpatterns = [
    path('my-registrations/', views.MyRegistrationsView.as_view(), name='my-registrations'),
    path('dashboard-stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('', include(router.urls)),
]
