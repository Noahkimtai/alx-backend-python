from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


class User(models.Model):
    """Represent a user in the messaging app"""

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, unique=True, null=False, db_index=True)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(
        max_length=20, choices=("guest", "host", "admin"), null=False
    )
    created_at = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    """Messages between users"""

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now)


class Conversation(models.Model):
    """Conversations between users"""

    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, db_index=True
    )
    participants_id = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)
