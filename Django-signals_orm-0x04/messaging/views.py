from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets
from rest_framework import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

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

    def get_thread(self, message):
        replies = (
            message.replies.all()
            .select_related("sender", "receiver")
            .prefetch_related("replies")
        )
        return {
            "id": message.id,
            "sender": str(message.sender),
            "receiver": str(message.receiver),
            "content": message.content,
            "replies": [self.get_thread(reply) for reply in replies],
        }

    @action(detail=False, methods=["get"])
    def threads(self, request):
        user = request.user

        root_messages = (
            Message.objects.filter(parent_message__isnull=True)
            .filter(Q(sender=user) | Q(receiver=user))
            .select_related("sender", "receiver")
            .prefetch_related("replies")
        )

        thread_data = [self.get_thread(msg) for msg in root_messages]
        return Response(thread_data)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    username = user.username
    user.delete()
    return Response({"message": f"User '{username}' deleted successfully."})
