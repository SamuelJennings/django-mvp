"""Basic smoke tests for mvp package."""

import pytest
from django.apps import apps


def test_app_config():
    """Test that the app is properly configured."""
    app_config = apps.get_app_config("mvp")
    assert app_config.name == "mvp"
    assert app_config.verbose_name == "Cotton Layouts"


def test_app_installed():
    """Test that the app is in INSTALLED_APPS."""
    assert apps.is_installed("mvp")


@pytest.mark.django_db
def test_basic_import():
    """Test that the package can be imported."""
    import mvp

    assert mvp.__version__ == "0.1.0"
