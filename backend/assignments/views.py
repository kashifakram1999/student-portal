from rest_framework import generics, permissions
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer
from users.permissions import IsTeacherUser, IsStudentUser
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from notifications.models import Notification
from courses.models import Enrollment
from django_filters.rest_framework import DjangoFilterBackend

# Teachers create assignments
class AssignmentCreateView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacherUser]

    def perform_create(self, serializer):
        assignment = serializer.save(created_by=self.request.user)
        enrolled_students = Enrollment.objects.filter(course=assignment.course).select_related('student')

        notifications = [
            Notification(
                recipient=enroll.student,
                title=f"New Assignment: {assignment.title}",
                message=f"A new assignment has been posted in {assignment.course.name}.",
                sender=self.request.user
            ) for enroll in enrolled_students
        ]
        Notification.objects.bulk_create(notifications)
        

# All users can list assignments
class AssignmentListView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']

# Students submit assignments
class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudentUser]

    def perform_create(self, serializer):
        assignment = serializer.validated_data['assignment']
        if assignment.due_date < timezone.now().date():
            raise ValidationError("The deadline for this assignment has passed.")

        submission = serializer.save(student=self.request.user)

        Notification.objects.create(
            recipient=assignment.created_by,
            title=f"New Submission for {assignment.title}",
            message=f"{self.request.user.username} submitted their work.",
            sender=self.request.user
        )

# Teachers view submissions to their assignments
class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsTeacherUser]

    def get_queryset(self):
        return Submission.objects.filter(assignment__created_by=self.request.user)

# Teachers grade/update submissions
class SubmissionUpdateView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsTeacherUser]
    lookup_field = 'pk'
