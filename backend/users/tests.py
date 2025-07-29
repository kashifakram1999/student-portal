from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User

class AuthTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            "email": "student1@example.com",
            "username": "student1",
            "password": "pass1234",
            "role": "student"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_login_success(self):
        user = User.objects.create_user(
            email="student2@example.com",
            username="student2",
            password="pass1234",
            role="student"
        )
        url = reverse('login')
        data = {
            "email": "student2@example.com",
            "password": "pass1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
