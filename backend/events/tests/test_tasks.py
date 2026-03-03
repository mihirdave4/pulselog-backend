from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from events.models import Event
from events.tasks import process_event, process_bulk_events

User = get_user_model()


class ProcessEventTaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="task@test.com",
            name="Task User",
            password="password"
        )

    @patch("events.tasks.increment_event_counter")
    def test_process_event_creates_event_and_calls_increment(self, mock_increment):
        data = {
            "event_type": "LOGIN",
            "payload": {"ip": "127.0.0.1"}
        }

        process_event(
            user_id=self.user.id,
            data=data
        )

        self.assertEqual(Event.objects.count(), 1)

        event = Event.objects.first()
        self.assertEqual(event.event_type, "LOGIN")
        self.assertEqual(event.payload["ip"], "127.0.0.1")

        mock_increment.assert_called_once_with(
            user_id=self.user.id,
            event_type="LOGIN"
        )


class ProcessBulkEventTaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="bulk@test.com",
            name="Bulk User",
            password="password"
        )

    @patch("events.tasks.increment_event_counter")
    def test_process_bulk_events(self, mock_increment):
        events = [
            {
                "event_type": "LOGIN",
                "payload": {"device": "mobile"}
            },
            {
                "event_type": "LOGOUT",
                "payload": {"device": "web"}
            }
        ]

        process_bulk_events(
            user_id=self.user.id,
            events=events
        )

        self.assertEqual(Event.objects.count(), 2)

        self.assertEqual(mock_increment.call_count, 2)

        mock_increment.assert_any_call(
            user_id=self.user.id,
            event_type="LOGIN"
        )

        mock_increment.assert_any_call(
            user_id=self.user.id,
            event_type="LOGOUT"
        )
