from django.urls import path
from .views import EventIngestView,BulkEventIngestView

urlpatterns = [
    path('ingest/', EventIngestView.as_view()),
    path("ingest/bulk/", BulkEventIngestView.as_view(), name="bulk-ingest"),


]
