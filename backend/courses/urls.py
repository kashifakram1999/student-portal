from django.urls import path
from .views import CourseCreateView, CourseListView, EnrollCourseView

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('create/', CourseCreateView.as_view(), name='course-create'),
    path('enroll/', EnrollCourseView.as_view(), name='course-enroll'),
]
