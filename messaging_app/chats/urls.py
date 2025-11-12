from django.urls import path, include
from rest_framework import routers

from .views import ConversationViewSet, MessageViewset, UserViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewset, basename="message")
router.register(r"users", UserViewSet, basename="user")
urlpatterns = [
    path("", include(router.urls)),
]
