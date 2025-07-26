from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from users.permissions import IsAdminUser, IsStudentUser, IsTeacherUser


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({"user": serializer.data, "token": token}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = get_tokens_for_user(user)
        return Response({"user": {"email": user.email, "role": user.role}, "token": token})


class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        from courses.models import Course, Enrollment
        from users.models import User

        return Response({
            "total_courses": Course.objects.count(),
            "total_students": User.objects.filter(role='student').count(),
            "total_teachers": User.objects.filter(role='teacher').count(),
            "total_enrollments": Enrollment.objects.count(),
        })

class StudentDashboardView(APIView):
    permission_classes = [IsStudentUser]

    def get(self, request):
        user = request.user
        from courses.models import Enrollment
        my_enrollments = Enrollment.objects.filter(student=user)

        return Response({
            "my_enrollments": my_enrollments.count(),
            "courses": [enroll.course.name for enroll in my_enrollments]
        })

class TeacherDashboardView(APIView):
    permission_classes = [IsTeacherUser]

    def get(self, request):
        user = request.user
        from courses.models import Course

        my_courses = Course.objects.filter(teacher=user)
        return Response({
            "my_courses": my_courses.count(),
            "course_names": [course.name for course in my_courses]
        })