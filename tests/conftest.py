"""
Test fixtures for django-cotton-layouts test suite.

This module provides reusable fixtures for testing layout components.
"""

import pytest
from django.template import Context
from django.template.loader import get_template
from django.test import RequestFactory


@pytest.fixture
def render_cotton_component():
    """
    Fixture that provides a helper function to render Django-Cotton components.

    Usage:
        def test_something(render_cotton_component):
            html = render_cotton_component(
                'test_template.html',
                context={'page_config': {...}}
            )
    """

    def _render(template_name_or_string, context=None):
        """Render a template by name or string with optional context."""
        if context is None:
            context = {}

        # Ensure page_config exists in context for components that need it
        if "page_config" not in context:
            context["page_config"] = {
                "brand": {
                    "text": "Test Site",
                    "icon_light": None,
                    "icon_dark": None,
                },
                "navigation": {
                    "sidebar": {},
                    "navbar": {},
                },
            }

        # Ensure request exists for Cotton components
        if "request" not in context:
            factory = RequestFactory()
            context["request"] = factory.get("/")

        # Try to load as a template file first
        try:
            template = get_template(template_name_or_string)
            return template.render(context)
        except Exception:
            # If that fails, it might be inline template string
            # Create a temporary template file for testing
            from django.template import Template

            template = Template("{% load cotton %}" + template_name_or_string)
            return template.render(Context(context))

    return _render


@pytest.fixture
def inner_layout_context():
    """
    Fixture providing default context for inner layout component tests.

    Returns a dict with page_config and common test data.
    """
    return {
        "page_config": {
            "brand": {
                "text": "Test Site",
                "icon_light": None,
                "icon_dark": None,
            },
            "navigation": {
                "sidebar": {},
                "navbar": {},
            },
        },
        "test_content": "<h1>Test Content</h1><p>This is test content.</p>",
        "test_sidebar_nav": """
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>
        """,
        "test_sidebar_meta": """
            <aside>
                <h4>Related Links</h4>
                <ul>
                    <li><a href="/related1">Related 1</a></li>
                    <li><a href="/related2">Related 2</a></li>
                </ul>
            </aside>
        """,
    }


@pytest.fixture
def mock_viewport_sizes():
    """
    Fixture providing common viewport size test data.

    Returns a dict mapping breakpoint names to pixel widths.
    """
    return {
        "mobile": 375,
        "sm": 576,
        "md": 768,
        "lg": 992,
        "xl": 1200,
        "xxl": 1400,
        "desktop": 1920,
    }
