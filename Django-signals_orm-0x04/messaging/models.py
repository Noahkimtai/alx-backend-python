from django.db import models
from django.contrib import User


class Message(models.Model):

    sender = models.ForeignKey(
        User, related_name="sent_message", on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User, related_name="received_message", on_delete=models.CASCADE
    )

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"
