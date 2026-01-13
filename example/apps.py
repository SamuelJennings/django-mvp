"""Example app configuration."""

from django.apps import AppConfig


class ExampleConfig(AppConfig):
    """Example application configuration.

    Automatically loads menu definitions on app startup to populate
    the navigation menu with example items.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "example"

    def ready(self):
        """Initialize the app when Django starts.

        This method is called once Django has finished loading all apps.
        It's the perfect place to import menu definitions and other
        app initialization code.
        """
        # Import menu definitions to register them with AppMenu
        # This must happen in ready() to ensure all apps are loaded
        try:
            from . import menus  # noqa: F401
        except ImportError:
            # Handle case where menus.py doesn't exist or has errors
            pass

    verbose_name = "Example"
