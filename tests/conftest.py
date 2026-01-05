"""
Test fixtures for django-cotton-layouts test suite.

This module provides reusable fixtures for testing layout components.
"""

import pytest
from django.template import Context
from django.template.loader import get_template
from django.test import RequestFactory


def render_component(request, component_name, context=None, **kwargs):
    """
    Render a Cotton component from a view with context values passed as attributes.

    This helper allows you to render Cotton components programmatically from views,
    which is especially useful for HTMX partial responses. The signature matches
    Django's render() convention: render_component(request, component_name, context).

    Args:
        request: HttpRequest object (required, like Django's render())
        component_name: Component name in dotted notation (e.g., "ui.button" or "button")
        context: Dictionary of data to pass to the component as attributes
        **kwargs: Alternative way to pass component attributes

    Returns:
        Rendered HTML string

    Example:
        # Using context dict (matches Django's render pattern)
        render_component(request, "button", {"pk": 123, "label": "Click me"})

        # Using kwargs (most common HTMX pattern)
        render_component(request, "button", pk=123, label="Click me")

        # Mix dict and kwargs
        render_component(request, "user_card", {"user": user}, extra_class="highlight")
    """
    from django.template import RequestContext, Template

    # Merge context dict and kwargs
    if context is None:
        context = kwargs
    elif kwargs:
        context = {**context, **kwargs}
    else:
        context = dict(context)  # Make a copy to avoid mutating original

    # Build minimal template using :attrs to pass all attributes at once
    tag_name = component_name.replace(".", "-")
    template_str = f'{{% cotton {tag_name} :attrs="cotton_component_attrs" / %}}'
    template = Template(template_str)

    # Prepare render context (keep original context plus our attrs dict)
    render_context = {**context, "cotton_component_attrs": context}

    # Create RequestContext (request is now always provided)
    ctx = RequestContext(request, render_context)

    return template.render(ctx)


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

            template = Template("" + template_name_or_string)
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
