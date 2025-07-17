# chats/urls.py

from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path("", include(router.urls)),
]