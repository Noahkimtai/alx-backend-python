from django.test import TestCase
from django.contrib.auth.models import User
from messaging.models import Message, Notification


class MessageSignal(TestCase):

    def test_notification_created(self):
        user1 = User.objects.create(username="alice")
        user2 = User.objects.create(username="bob")

        msg = Message.objects.create(
            sender=user1, receiver=user2, content="hello!"
        )

        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, user2)
        self.assertEqual(notification.message, msg)
