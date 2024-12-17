from django.utils.timezone import now
from datetime import timedelta

class SessionSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Set the session cookie to never expire if the user is authenticated
            request.session.set_expiry(0)  # '0' means the session never expires.
            request.session.modified = True
        else:
            # Set session expiration for non-authenticated users (1 hour for example)
            request.session.set_expiry(3600)  # 1 hour
            request.session.modified = True

        response = self.get_response(request)
        return response