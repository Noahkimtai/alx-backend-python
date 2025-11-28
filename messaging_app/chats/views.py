from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .filters import MessageFilter
from .permissions import IsParticipantOfConversation

from .pagination import SmallResultsSetPagination

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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = SmallResultsSetPagination

    def perform_create(self, serializer):
        participant_ids = self.request.data.get("participant_ids", [])
        conversation = serializer.save()
        if participant_ids:
            conversation.participants.set(participant_ids)


class MessageViewset(viewsets.ModelViewSet):
    """Manage messages"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = SmallResultsSetPagination

    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    # def get_queryset(self):
    #     return Message.objects.filter(
    #         Conversation_participants=self.request.user
    #     )


class UserViewSet(viewsets.ModelViewSet):
    "manage messages"

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = SmallResultsSetPagination
