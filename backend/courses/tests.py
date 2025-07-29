from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)

class CourseTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email='admin@example.com', username='admin', password='admin123', role='admin')
        self.student = User.objects.create_user(email='student@example.com', username='student', password='pass1234', role='student')

    def test_admin_can_create_course(self):
        token = get_token(self.admin)
        url = reverse('course-create')
        data = {
            "name": "Math 101",
            "description": "Intro to Math"
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_student_cannot_create_course(self):
        token = get_token(self.student)
        url = reverse('course-create')
        data = {
            "name": "Physics",
            "description": "Intro to Physics"
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)
