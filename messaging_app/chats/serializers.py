from django.db import models
from django.utils import timezone
import uuid
from rest_framework import serializers
from .models import Conversation, Message, User

# from messaging_app.chats.models import Conversation, Message, User.


class UserSerializer(serializers.HyperlinkSerializer):
    """Represent a user in the messaging app"""

    class meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]


class MessageSerializer(serializers.HyperlinkSerializer):
    """Messages between users"""

    sender = UserSerializer(read_only=True)

    class meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "sent_at"]

    read_only_fields = ["message_id", "sent_at", "sender"]


class ConversationSerializer(serializers.HyperlinkSerializer):
    """Conversations between users"""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class meta:
        model = Conversation
        fields = ["conversation_id", "participants", "messages", "created_at"]
        read_only_fields = ["conversation_id", "created_at"]
