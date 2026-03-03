from django.urls import path
from .views import MyDailyStatsView, GlobalDailyStatsView

urlpatterns = [
    path('me/daily/', MyDailyStatsView.as_view()),
    path('global/daily/', GlobalDailyStatsView.as_view()),
]
