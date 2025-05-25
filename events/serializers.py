from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'location', 'is_recurring', 'recurrence_pattern']

class EventCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    location = serializers.CharField(required=False, allow_blank=True)
    is_recurring = serializers.BooleanField(default=False)
    recurrence_pattern = serializers.CharField(required=False, allow_blank=True)

class BulkEventCreateSerializer(serializers.ListSerializer):
    child = EventCreateSerializer()

class ShareUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=['OWNER', 'EDITOR', 'VIEWER'])

class EventParticipantSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    role = serializers.ChoiceField(choices=['OWNER', 'EDITOR', 'VIEWER'])

class EventParticipantEntrySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=["OWNER", "EDITOR", "VIEWER"])

class EventShareSerializer(serializers.Serializer):
    users = serializers.ListField(
        child=EventParticipantEntrySerializer(),
        allow_empty=False
    )

class BulkEventSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    location = serializers.CharField(required=False, allow_blank=True)
    is_recurring = serializers.BooleanField(default=False)
    recurrence_pattern = serializers.CharField(required=False, allow_blank=True)