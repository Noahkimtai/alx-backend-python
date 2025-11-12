from django.urls import path, include
from rest_framework import routers

from messaging_app.chats.views import ConversationViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet)

urlpatterns = [
    path("/", include(router.urls)),
    path("api_auth/", include("rest_framework.urls", namespace="rest_framework")),
]
