from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DailyUserEventCount
from .serializers import DailyEventStatsSerializer
from django.db.models import Sum

class MyDailyStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = DailyUserEventCount.objects.filter(
            user=request.user
        ).order_by('-date')

        serializer = DailyEventStatsSerializer(qs, many=True)
        return Response(serializer.data)

class GlobalDailyStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            DailyUserEventCount.objects
            .values('date', 'event_type')
            .annotate(total=Sum('count'))
            .order_by('-date')
        )

        return Response(qs)
