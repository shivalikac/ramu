"""
URL configuration for ramu project.

This module defines the URL patterns for the Django project.
It maps different URL paths to corresponding views.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin 
from django.urls import path, include  

# Define the main URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Route for the Django admin panel
    path('', include('accounts.urls')),  # Include URL patterns from the 'accounts' app
]
