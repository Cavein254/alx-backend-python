from django.urls import path
from .views import DeleteUserView, ConversationView

urlpatterns = [
    path('conversations/', ConversationView.as_view(), name='conversations'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
]
