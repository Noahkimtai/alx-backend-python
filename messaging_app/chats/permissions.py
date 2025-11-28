from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Only allow users who are participants of the conversation access to messages of the conversation
    """

    def has_permission(self, request, view):
        # user must be authenticated globally
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """
        obj access permission
        obj can be either Message or Conversation.
        For Message: obj.conversation
        For Conversation: obj
        """

        # For conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()
        # For messages
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()
        return False
