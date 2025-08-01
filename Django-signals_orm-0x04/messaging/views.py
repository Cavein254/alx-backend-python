from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Q

from .models import Message
from .serializers import MessageSerializer, MessageReplySerializer
from django.db.models import Prefetch

User = get_user_model()

class ConversationView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            Message.objects.filter(receiver=user, parent_message__isnull=True)
            .select_related('sender', 'receiver', 'edited_by')
            .prefetch_related(
                Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
            )
            .order_by('-timestamp')
        )
@method_decorator(cache_page(60), name='get')
class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all top-level messages (no parent) for the logged-in user
        messages = (
            Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))  
            .select_related('sender', 'receiver')         
            .prefetch_related('replies')                  
        )
        serializer = MessageReplySerializer(messages, many=True)
        return Response(serializer.data)
        

    def get_message_with_replies(self, message):
        """ Recursively fetch message replies """
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "replies": [self.get_message_with_replies(reply) for reply in message.replies.all()]
        }

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        username = user.username
        user.delete()  # Triggers the post_delete signal
        return Response({"message": f"User {username} and related data deleted successfully"}, status=status.HTTP_200_OK)

class UnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_messages = Message.unread.for_user(request.user)
        serializer = MessageReplySerializer(unread_messages, many=True)
        return Response(serializer.data)