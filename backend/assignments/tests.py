from rest_framework.test import APITestCase
from users.models import User
from courses.models import Course
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
import datetime

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)

class AssignmentTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(email='teacher@example.com', username='teacher', password='teacher123', role='teacher')
        self.course = Course.objects.create(name='CS101', description='Intro', teacher=self.teacher)

    def test_teacher_can_create_assignment(self):
        token = get_token(self.teacher)
        url = reverse('assignment-create')
        data = {
            "title": "Assignment 1",
            "description": "Do work",
            "due_date": str(datetime.date.today() + datetime.timedelta(days=5)),
            "course": self.course.id
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)
