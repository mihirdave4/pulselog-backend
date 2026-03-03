from celery import shared_task
from django.db import transaction

from .models import Event
from analytics.services import increment_event_counter


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=3)
def process_event(self, user_id, data):
    event = Event.objects.create(
        user_id=user_id,
        event_type=data["event_type"],
        payload=data["payload"]
    )

    increment_event_counter(
        user_id=user_id,
        event_type=event.event_type
    )


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def process_bulk_events(self, user_id, events):
    with transaction.atomic():
        for event in events:
            Event.objects.create(
                user_id=user_id,
                event_type=event["event_type"],
                payload=event["payload"]
            )

            increment_event_counter(
                user_id=user_id,
                event_type=event["event_type"]
            )
