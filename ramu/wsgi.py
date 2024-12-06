"""
WSGI config for ramu project.

This file serves as the entry point for WSGI-compatible web servers to
serve the Django project. It exposes the WSGI callable as a module-level 
variable named ``application``.
"""

import os  
from django.core.wsgi import get_wsgi_application  

# Set the default settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ramu.settings')

# WSGI application callable
# This application object is used by WSGI servers to forward 
# requests to the Django application. It acts as an interface
# between the server and the Django project.
application = get_wsgi_application()
