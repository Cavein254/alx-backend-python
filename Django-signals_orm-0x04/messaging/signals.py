from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from messaging.models import Message, Notification, MessageHistory

def create_notification(sender, instance, created, **kwargs):
    print("📩 Signal fired for Message") 
    if created:
        Notification.objects.create(
            user = instance.receiver,  # Assuming 'receiver' is the field for the recipient
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
            instance.edited = True
        except Message.DoesNotExist:
            pass