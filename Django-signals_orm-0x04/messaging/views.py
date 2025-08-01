# messaging/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == "POST":
        request.user.delete()  # This will trigger the post_delete signal
        return redirect('home')  # Or redirect to a goodbye page

    return redirect('profile')
