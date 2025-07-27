import logging
from datetime import datetime, timedelta
from collections import defaultdict
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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Stores timestamps per IP
        self.ip_message_log = defaultdict(list)

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Apply logic only for POST requests (e.g., sending messages)
        if request.method == 'POST' and request.path.startswith('/chat/'):
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            # Remove timestamps older than 1 minute
            recent_timestamps = [t for t in self.ip_message_log[ip] if t > window_start]
            self.ip_message_log[ip] = recent_timestamps

            if len(recent_timestamps) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Only 5 messages allowed per minute.")

            # Log current message timestamp
            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '')