import os
from django.core.asgi import get_asgi_application

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ayur_rich.settings')

# Define the ASGI application for HTTP only
application = get_asgi_application()