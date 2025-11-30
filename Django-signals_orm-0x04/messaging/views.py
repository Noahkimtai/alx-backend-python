from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets
from rest_framework import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from serializers import MessageSerializer, NotificationSerializer
from models import Notification, Message


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user) | Message.objects.filter(
            sender=self.request.user
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
            .filter(Q(sender=request.user) | Q(receiver=user))
            .select_related("sender", "receiver")
            .prefetch_related("replies")
        )

        thread_data = [self.get_thread(msg) for msg in root_messages]
        return Response(thread_data)

    @action(detail=False, methods=["get"])
    def unread(self, request):
        user = request.user
        unread_messages = Message.unread.for_user(user)
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        message = get_object_or_404(Message, pk=pk, receiver=request.user)
        message.read = True
        message.save()
        return Response({"status": "marked as read"})


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
