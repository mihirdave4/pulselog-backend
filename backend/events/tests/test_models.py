from django.test import TestCase
from django.contrib.auth import get_user_model
from events.models import Event  # adjust import if needed

User = get_user_model()

class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123"
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertTrue(user.is_active)


class EventModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="event@test.com",
            name="Event User",
            password="password"
        )

    def test_create_event(self):
        event = Event.objects.create(
            user=self.user,
            event_type="LOGIN",
            payload={"ip": "127.0.0.1"}
        )   

        self.assertEqual(event.user.email, "event@test.com")
        self.assertEqual(event.event_type, "LOGIN")
