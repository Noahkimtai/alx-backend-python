from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib import User

from messaging.models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Create a notification when a new message is sent"""

    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def save_previous_message(sender, instance, **kwargs):
    """Before a message is updated, save the old content to MessageHistory"""
    # For new message nothing to log
    if not instance.pk:
        return
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Log when content change
    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content,
            edited_by=instance.sender,
        )
        instance.edited = True  # Mark message as edited


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).update(edited_by=None)

    print(f"Cleanup completed for deleted user: {instance.username}")
