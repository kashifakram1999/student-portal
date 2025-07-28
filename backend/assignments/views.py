from rest_framework import generics, permissions
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer
from users.permissions import IsTeacherUser, IsStudentUser

# Teachers create assignments
class AssignmentCreateView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacherUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# All users can list assignments
class AssignmentListView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

# Students submit assignments
class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudentUser]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

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
