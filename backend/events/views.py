from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import BulkEventSerializer,BulkEventIngestSerializer,EventSerializer
from .tasks import process_event,process_bulk_events
from .services import ingest_event,ingest_bulk_events
from .serializers import BulkEventSerializer


class EventIngestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        accepted = ingest_event(
            user_id=request.user.id,
            event_data=serializer.validated_data
        )

        if not accepted:
            return Response(
                {"status": "duplicate"},
                status=200
            )

        return Response(
            {"status": "accepted"},
            status=202
        )
    
    
class BulkEventIngestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BulkEventIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        accepted = ingest_bulk_events(
            user_id=request.user.id,
            events=serializer.validated_data["events"]
        )

        return Response(
            {
                "status": "accepted",
                "received": len(serializer.validated_data["events"]),
                "accepted": accepted,
            },
            status=status.HTTP_202_ACCEPTED,
        )
