from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    # Auth
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Teachers & students
    path('teachers/', views.TeacherListView.as_view(), name='teacher-list'),
    path('my-students/', views.MyStudentsView.as_view(), name='my-students'),
    path('my-students/<int:pk>/remove/', views.RemoveStudentView.as_view(), name='remove-student'),

    # Teacher requests (participant → teacher)
    path('teacher-requests/', views.TeacherRequestView.as_view(), name='teacher-requests'),
    path('teacher-requests/<int:pk>/', views.TeacherRequestView.as_view(), name='teacher-request-delete'),
    path('teacher-requests/<int:pk>/<str:action>/', views.TeacherRequestActionView.as_view(), name='teacher-request-action'),

    # Users CRUD (admin)
    path('', include(router.urls)),
]
