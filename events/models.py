from django.db import models
from django.core.cache import cache

# Create your models here.
# events/models.py
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Event(models.Model):
    RECURRING_PATTERNS = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=255, blank=True, null=True, choices= RECURRING_PATTERNS)  # e.g., 'daily', 'weekly', iCal rule etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    participants = models.ManyToManyField(User, through='EventParticipant', related_name='events')
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.title}-{self.location}"
    
    def clear_cache(self):
        # Invalidate cache for all users who participated in this event
        for user in self.participants.all():
            cache_key = f"event_detail_view_{self.id}_user_{user.id}"
            cache.delete(cache_key)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clear_cache()

    def delete(self, *args, **kwargs):
        self.clear_cache()
        super().delete(*args, **kwargs)


class EventParticipant(models.Model):
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('EDITOR', 'Editor'),
        ('VIEWER', 'Viewer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} ({self.role}) in {self.event.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f"event_participants_{self.event_id}")

    def delete(self, *args, **kwargs):
        event_id = self.event_id
        super().delete(*args, **kwargs)
        cache.delete(f"event_participants_{event_id}")


