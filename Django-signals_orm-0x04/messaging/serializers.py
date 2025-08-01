# messaging/serializers.py
from rest_framework import serializers
from .models import Message

class RecursiveMessageSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return MessageSerializer(instance, context=self.context).data


class MessageSerializer(serializers.ModelSerializer):
    replies = RecursiveMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'edited_by', 'parent_message', 'replies']


class MessageReplySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'replies']

    def get_replies(self, obj):
        return MessageReplySerializer(obj.replies.all(), many=True).data