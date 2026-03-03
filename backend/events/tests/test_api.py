from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from events.models import Event
import uuid
from django.test import override_settings

User = get_user_model()

@override_settings(    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True
)
class EventAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="api@test.com",
            name="API User",
            password="password"
        )

        self.client.force_authenticate(user=self.user)

    def test_create_event(self):
        response = self.client.post(
            "/api/events/ingest/",
            {
                 "event_id": str(uuid.uuid4()),
                "event_type": "LOGIN",
                "payload": {"device": "mobile"}
            },
            format="json"
        )
        print(response.data)
        self.assertEqual(response.status_code, 202)     

        # self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), 1)
