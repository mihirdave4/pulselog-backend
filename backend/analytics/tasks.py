from celery import shared_task
from django.db import transaction
from django.db.models import F
from datetime import date

from .models import DailyUserEventCount
from .redis import redis_client
from .services import get_all_analytics_keys


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def flush_analytics_to_db(self):
    keys = get_all_analytics_keys()

    for key in keys:
        _, user_id, day, event_type = key.split(":")

        count = redis_client.get(key)
        if not count:
            continue

        count = int(count)

        with transaction.atomic():
            obj, _ = DailyUserEventCount.objects.get_or_create(
                user_id=user_id,
                date=day,
                event_type=event_type,
            )

            obj.count = F("count") + count
            obj.save()

        redis_client.delete(key)
