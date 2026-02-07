"""Tests for mvp.utils module."""

import pytest
from django.test import override_settings

from mvp.utils import app_is_installed


class TestAppIsInstalled:
    """Tests for the app_is_installed utility function."""

    def test_installed_app_returns_true(self):
        """Test that an installed app returns True."""
        # Django's built-in apps should always be installed
        assert app_is_installed("django.contrib.admin") is True
        assert app_is_installed("django.contrib.auth") is True

    def test_installed_app_by_config_name_returns_true(self):
        """Test that an installed app can be checked by its config name."""
        # The mvp app is installed, check by its config name
        assert app_is_installed("mvp") is True
        assert app_is_installed("example") is True

    def test_not_installed_app_returns_false(self):
        """Test that a non-installed app returns False."""
        assert app_is_installed("nonexistent_app") is False
        assert app_is_installed("fake_app_123") is False

    def test_mvp_app_is_installed(self):
        """Test that the mvp app itself is detected as installed."""
        assert app_is_installed("mvp") is True

    def test_example_usage_pattern(self):
        """Test the example usage pattern from the docstring."""
        # This demonstrates the intended usage pattern
        CRISPY_FORMS = app_is_installed("crispy_forms")
        assert CRISPY_FORMS is True  # Installed in test environment

        DJANGO_ADMIN = app_is_installed("django.contrib.admin")
        assert DJANGO_ADMIN is True  # Built-in Django app

        FAKE_APP = app_is_installed("fake_app")
        assert FAKE_APP is False  # Not installed

    def test_module_level_constant_pattern(self):
        """Test that the function can be used to create module-level constants."""
        # This pattern is commonly used at the top of views.py modules
        HAS_DJANGO_ADMIN = app_is_installed("django.contrib.admin")
        HAS_FAKE_APP = app_is_installed("fake_app_that_does_not_exist")

        assert HAS_DJANGO_ADMIN is True
        assert HAS_FAKE_APP is False

    def test_various_installed_apps(self):
        """Test detection of various apps installed in test environment."""
        # Test some apps that are in the test INSTALLED_APPS
        assert app_is_installed("django_cotton") is True
        assert app_is_installed("cotton_bs5") is True
        assert app_is_installed("easy_icons") is True
        assert app_is_installed("flex_menu") is True

