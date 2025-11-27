from rest_framework import viewsets


from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    UserSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    Manage conversations (list, create, retrieve, etc.)
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def perform_create(self, serializer):
        """Create a new conversation"""
        conversation = serializer.save()
        return conversation


class MessageViewset(viewsets.ModelViewSet):
    """Manage messages"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """Create a new message"""

        serializer.save()


class UserViewSet(viewsets.ModelViewSet):
    "manage messages"

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        """Create a new message"""
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = Conversation.objects.get(pk=conversation_id)
        serializer.save(conversation=conversation)
