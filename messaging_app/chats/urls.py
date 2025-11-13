from django.urls import path, include
from rest_framework_nested import routers

from .views import ConversationViewSet, MessageViewset, UserViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewset, basename="message")
router.register(r"users", UserViewSet, basename="user")
# messages belong to conversations
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup="conversation")
conversations_router.register(r'messages', MessageViewset, basename = "conversation-messages")
urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversations_router.urls)),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
]
