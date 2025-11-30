from rest_framework import serializers
from .models import Message, Notification, MessageHistory
from serializers import MessageHistorySerializer


class MessageSerializer:
    history = MessageHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fileds = ["id", "sender", "receiver", "timestamp"]
        read_only_fields = [
            "id",
            "sender",
            "receiver",
            "content",
            "created_at",
            "updated_at",
            "edited",
            "history",
        ]


class NotificationSerializer:
    class Meta:
        model = Notification
        fileds = ["id", "user", "message", "is_read" "timestamp"]
        read_only_fields = ["timestamp"]


class MessageHistorySerializer(serializers.ModelSerializer):
    edited_by = serializers.StringRelatedField()

    class meta:
        model = MessageHistory
        fields = ["old_content", "edited_by", "edited_at"]
