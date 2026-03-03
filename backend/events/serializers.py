from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    event_id = serializers.UUIDField()
    event_type = serializers.CharField(max_length=100)
    payload = serializers.JSONField()

class SingleEventSerializer(serializers.Serializer):
    event_id = serializers.UUIDField()
    event_type = serializers.CharField(max_length=100)
    payload = serializers.JSONField()

class BulkEventSerializer(serializers.Serializer):
    events = SingleEventSerializer(many=True)

class EventIngestSerializer(serializers.Serializer):
    event_id = serializers.UUIDField()
    event_type = serializers.CharField(max_length=50)
    payload = serializers.JSONField()


class BulkEventIngestSerializer(serializers.Serializer):
    events = EventIngestSerializer(many=True, allow_empty=False)