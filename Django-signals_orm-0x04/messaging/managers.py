from messaging_app.chats import models


class UnreadMessagesManager(models.Manager):
    """Manager to return only unread messages for a given user."""

    def for_user(self, user):
        # Only retrieve unread messages for this user
        return self.filter(receiver=user, read=False).only(
            "id", "sender", "message_body", "sent_at", "parent_message"
        )
