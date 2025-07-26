from django.urls import path
from .views import RegisterView, LoginView

from .views import (
    AdminDashboardView,
    StudentDashboardView,
    TeacherDashboardView,
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
urlpatterns += [
    path('dashboard/admin/', AdminDashboardView.as_view()),
    path('dashboard/student/', StudentDashboardView.as_view()),
    path('dashboard/teacher/', TeacherDashboardView.as_view()),
]