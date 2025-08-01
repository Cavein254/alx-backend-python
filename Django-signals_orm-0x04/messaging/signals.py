from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message, Notification

def create_notification(sender, instance, created, **kwargs):
    print("📩 Signal fired for Message") 
    if created:
        Notification.objects.create(
            user=getattr(instance, 'receiver', getattr(instance, 'recipient')),
            message=instance
        )