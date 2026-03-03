from rest_framework import serializers
from .models import DailyUserEventCount


class DailyEventStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyUserEventCount
        fields = ('date', 'event_type', 'count')
