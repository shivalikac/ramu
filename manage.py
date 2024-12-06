#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os  
import sys

def main():
    """Run administrative tasks."""
    # Set the default Django settings module for the 'ramu' project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ramu.settings')
    
    try:
        # Import the Django management command executor
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an error if Django is not installed or configured properly
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command-line utility using the provided arguments
    execute_from_command_line(sys.argv)

# Entry point for the script
if __name__ == '__main__':
    main()