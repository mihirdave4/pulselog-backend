
from .tasks import process_event, process_bulk_events

from .tasks import process_event
from .redis import redis_client

EVENT_TTL = 60 * 60  # 1 hour

def ingest_event(user_id, event_data):
    event_id = str(event_data["event_id"])
    redis_key = f"event:{event_id}"

    # SETNX = set if not exists (atomic)
    locked = redis_client.set(
        redis_key,
        "1",
        nx=True,
        ex=EVENT_TTL
    )

    if not locked:
        # duplicate event
        return False

    process_event.delay(user_id, event_data)
    return True

# def ingest_event(*, user_id: int, event_data: dict):
    
#     process_event.delay(
#         user_id=user_id,
#         data=event_data
#     )


def ingest_bulk_events(user_id, events):
    accepted_events = []

    for event in events:
        redis_key = f"event:{event['event_id']}"

        is_new = redis_client.set(
            redis_key,
            "1",
            nx=True,
            ex=EVENT_TTL
        )

        if is_new:
            accepted_events.append(event)

    if accepted_events:
        process_bulk_events.delay(user_id, accepted_events)

    return len(accepted_events)
