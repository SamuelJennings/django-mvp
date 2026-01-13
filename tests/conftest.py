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


# ============================================================================
# Menu Testing Fixtures
# ============================================================================


@pytest.fixture
def menu_factory():
    """Factory for creating Menu instances with children."""
    from flex_menu import Menu

    def _create_menu(name="TestMenu", children=None):
        return Menu(name, children=children or [])

    return _create_menu


@pytest.fixture
def menu_item_factory():
    """Factory for creating MenuItem instances."""
    from flex_menu import MenuItem

    def _create_item(
        name,
        view_name=None,
        extra_context=None,
        children=None,
    ):
        return MenuItem(
            name=name,
            view_name=view_name,
            extra_context=extra_context or {},
            children=children or [],
        )

    return _create_item


@pytest.fixture
def adminlte_renderer():
    """Provides an instance of AdminLTERenderer for testing."""
    from mvp.renderers import AdminLTERenderer

    return AdminLTERenderer()


@pytest.fixture
def app_menu():
    """Provides a fresh AppMenu instance for testing."""
    from mvp.menus import AppMenu

    # Store original children before tests
    original_children = tuple(AppMenu.children)

    # Clear children for test
    for child in list(AppMenu.children):
        child.parent = None

    yield AppMenu

    # Restore original children after test
    for child in list(AppMenu.children):
        child.parent = None
    for child in original_children:
        child.parent = AppMenu
