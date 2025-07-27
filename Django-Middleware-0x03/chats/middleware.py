import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow access only between 6PM (18) and 9PM (21)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to the messaging app is restricted at this time.")

        return self.get_response(request)


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Check if the user is authenticated and has a valid role
        if user.is_authenticated:
            role = getattr(user, 'role', None)  # Assumes User model has a 'role' attribute
            if role in ['admin', 'moderator']:
                return self.get_response(request)

        return HttpResponseForbidden("Access denied: You do not have the required permissions.")
