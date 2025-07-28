from django.urls import path
from .views import (
    AssignmentCreateView,
    AssignmentListView,
    SubmissionCreateView,
    SubmissionListView,
    SubmissionUpdateView
)

urlpatterns = [
    path('assignments/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignments/create/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('submissions/create/', SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/grade/', SubmissionUpdateView.as_view(), name='submission-update'),
]
