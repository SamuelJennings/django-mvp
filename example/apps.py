"""Example app configuration."""

from django.apps import AppConfig


class ExampleConfig(AppConfig):
    """Example application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "example"
    verbose_name = "Example"
