from django.conf import settings
from django.db import models


class DailyUserEventCount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date = models.DateField()
    event_type = models.CharField(max_length=50)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date', 'event_type')
        indexes = [
            models.Index(fields=['date', 'event_type']),
        ]

    def __str__(self):
        return f"{self.user_id} {self.event_type} {self.date}"
