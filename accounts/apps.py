from django.apps import AppConfig

class AccountsConfig(AppConfig):
    """
    Configuration class for the 'accounts' app in a Django project.

    Attributes:
        default_auto_field (str): The type of auto field to use for primary keys.
        name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField' 
    name = 'accounts'