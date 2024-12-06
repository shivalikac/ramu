"""
ASGI config for ramu project.

This file contains the ASGI configuration required for deploying the Django application.
It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'ramu' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ramu.settings')

# Create the ASGI application callable to be used by the ASGI server
application = get_asgi_application()
