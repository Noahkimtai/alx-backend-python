from rest_framework import serializers
from .models import Message, Notification


class MessageSerializer:
    class Meta:
        model = Message
        fileds = ["id", "sender", "receiver", "timestamp"]
        read_only_fields = ["sender", "timestamp"]


class NotificationSerializer:
    class Meta:
        model = Notification
        fileds = ["id", "user", "message", "is_read" "timestamp"]
        read_only_fields = ["timestamp"]
