from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message, Notification

User = get_user_model()

class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender', email='sender@example.com', password='password123'
        )
        self.recipient = User.objects.create_user(
            username='recipient', email='recipient@example.com', password='password123'
        )

    def test_notification_created_on_message(self):
        self.assertEqual(Notification.objects.count(), 0)

        message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,  
            content="Hello recipient!"
        )

        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.recipient)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

    def test_multiple_messages_generate_notifications(self):
        for i in range(3):
            Message.objects.create(
                sender=self.sender,
                recipient=self.recipient,  
                content=f"Message {i}"
            )

        self.assertEqual(Notification.objects.count(), 3)
        for notif in Notification.objects.all():
            self.assertEqual(notif.user, self.recipient)
