from django.db import models
from django.contrib import User
from django.utils import timezone


class Message(models.Model):

    sender = models.ForeignKey(
        User, related_name="sent_message", on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User, related_name="received_message", on_delete=models.CASCADE
    )

    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=False)
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"History for message{self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"
