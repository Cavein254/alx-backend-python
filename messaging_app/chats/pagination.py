from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        # Extract conversation_id from URL kwargs
        conversation_id = self.kwargs.get('conversation_id') or self.request.query_params.get('conversation_id')
        if not conversation_id:
            raise NotFound(detail="conversation_id parameter is required")
        # Only return messages for this conversation where user is a participant
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        # Extract conversation and verify participation
        conversation_id = self.kwargs.get('conversation_id') or serializer.validated_data.get('conversation').id
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound(detail="Conversation not found")

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Save message with sender and conversation
        serializer.save(sender=self.request.user, conversation=conversation)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only show conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # On creation, ensure the creator is added as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return conversation
