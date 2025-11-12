from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


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
