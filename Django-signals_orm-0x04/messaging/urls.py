from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from views import MessageViewSet, NotificationViewSet, delete_user

router = DefaultRouter()
router.register("messages", MessageViewSet, basename="messages")
router.register("notification", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
    path("delete-account/", delete_user, name="delete_account"),
]
