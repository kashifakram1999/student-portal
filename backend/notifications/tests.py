# notifications/tests.py
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from notifications.models import Notification
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)

class NotificationTests(APITestCase):
    def setUp(self):
        Notification.objects.all().delete()
        self.client = APIClient()

        self.sender = User.objects.create_user(
            email='admin@example.com', username='admin', password='admin123', role='admin'
        )
        self.recipient = User.objects.create_user(
            email='student@example.com', username='student', password='pass1234', role='student'
        )

        self.sender_token = get_token(self.sender)
        self.recipient_token = get_token(self.recipient)

    def tearDown(self):
        Notification.objects.all().delete()

    def test_create_notification(self):
        url = reverse('notification-list-create')
        data = {
            "recipient": self.recipient.id,
            "title": "Test Notification",
            "message": "This is a test."
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.sender_token}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Notification.objects.count(), 1)

    def test_list_own_notifications(self):
        Notification.objects.create(
            recipient=self.recipient,
            title="Welcome!",
            message="Hello student",
            sender=self.sender
        )
        url = reverse('notification-list-create')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.recipient_token}')
        print("[DEBUG] Response data:", response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Now response.data is a list, no pagination
        self.assertEqual(response.data[0]['title'], "Welcome!")

    def test_user_cannot_see_others_notifications(self):
        Notification.objects.create(
            recipient=self.recipient,
            title="Private Message",
            message="You shouldn't see this",
            sender=self.sender
        )
        url = reverse('notification-list-create')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.sender_token}')
        print("[DEBUG] Response data:", response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)  # No notifications for sender
