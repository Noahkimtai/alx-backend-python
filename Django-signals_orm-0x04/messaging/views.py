from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import IsAuthenticated
from serializers import MessageSerializer, NotificationSerializer
from models import Notification, Message


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user) | Message.objects.filter(
            sender=user
        )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(sender=user)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)
