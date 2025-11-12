from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ConversationViewSet, MessageViewset

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewset, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
