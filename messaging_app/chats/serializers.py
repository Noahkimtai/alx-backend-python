from rest_framework import serializers
from .models import Conversation, Message, User

# from messaging_app.chats.models import Conversation, Message, User.


class UserSerializer(serializers.ModelSerializer):
    """Represent a user in the messaging app"""

    ROLE_CHOICES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]

    first_name = serializers.CharField(required=True, max_length=200)
    last_name = serializers.CharField(required=True, max_length=200)
    email = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(max_length=20)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "full_name",
        ]

    def get_full_name(self, obj):
        """Method to compute full_name on the fly"""
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    """Messages between users"""

    sender = UserSerializer(read_only=True)
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")

        return value

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"


class ConversationSerializer(serializers.ModelSerializer):
    """Conversations between users"""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = "__all__"
