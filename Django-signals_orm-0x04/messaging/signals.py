from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message, Notification

def create_notification(sender, instance, created, **kwargs):
    print("📩 Signal fired for Message") 
    if created:
        Notification.objects.create(
            user = instance.receiver,  # Assuming 'receiver' is the field for the recipient
            message=instance
        )