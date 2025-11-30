from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework import IsAuthenticated
from rest_framework.response import Response

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


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    username = user.username
    user.delete()
    return Response({"message": f"User '{username}' deleted successfully."})
