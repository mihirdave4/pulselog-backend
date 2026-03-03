from datetime import date
from .redis import redis_client

REDIS_ANALYTICS_PREFIX = "analytics"


def increment_event_counter(user_id, event_type):
    today = date.today().isoformat()
    key = f"{REDIS_ANALYTICS_PREFIX}:{user_id}:{today}:{event_type}"
    redis_client.incr(key)


def get_all_analytics_keys():
    return redis_client.keys(f"{REDIS_ANALYTICS_PREFIX}:*")
