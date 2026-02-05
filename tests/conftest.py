"""
Test fixtures for django-cotton-layouts test suite.

This module provides reusable fixtures for testing layout components.
"""

import pytest
from bs4 import BeautifulSoup
from django.test import RequestFactory
from django_cotton import render_component as cotton_render_component


@pytest.fixture
def render_component():
    """
    Fixture that renders Django-Cotton components and returns raw HTML.

    Automatically provides a request object to be DRY. Component variables
    are passed as kwargs.

    Usage:
        def test_something(render_component):
            html = render_component(
                'adminlte.small-box',
                title="Users",
                value=150,
                icon="users"
            )
            assert 'Users' in html
    """
    factory = RequestFactory()

    def _render(component_name, context=None, **kwargs):
        """
        Render a Cotton component with automatic request injection.

        Args:
            component_name: Component name in dotted notation (e.g., "adminlte.small-box")
            context: Optional context dict to pass as component attributes
            **kwargs: Component attributes (alternative to context dict)

        Returns:
            Rendered HTML string
        """
        request = factory.get("/")
        return cotton_render_component(request, component_name, context, **kwargs)

    return _render


@pytest.fixture
def render_component_soup():
    """
    Fixture that renders Django-Cotton components and returns BeautifulSoup parsed HTML.

    Automatically provides a request object and parses the result for easy testing.
    Component variables are passed as kwargs.

    Usage:
        def test_something(render_component_soup):
            soup = render_component_soup(
                'adminlte.small-box',
                title="Users",
                value=150,
                icon="users"
            )
            assert soup.find('h3').text == '150'
            assert soup.find('p').text == 'Users'
    """
    factory = RequestFactory()

    def _render(component_name, context=None, **kwargs):
        """
        Render a Cotton component with automatic request injection and parse with BeautifulSoup.

        Args:
            component_name: Component name in dotted notation (e.g., "adminlte.small-box")
            context: Optional context dict to pass as component attributes
            **kwargs: Component attributes (alternative to context dict)

        Returns:
            BeautifulSoup parsed HTML object
        """
        request = factory.get("/")
        html = cotton_render_component(request, component_name, context, **kwargs)
        return BeautifulSoup(html, "html.parser")

    return _render


@pytest.fixture
def page_layout_context():
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


@pytest.fixture
def request_context():
    """Provides a RequestContext with proper request object for template rendering."""
    factory = RequestFactory()

    def _get_context(context_dict=None):
        """
        Create a RequestContext with a fake request.

        Args:
            context_dict: Optional dict with additional context variables

        Returns:
            RequestContext instance
        """
        from django.template import RequestContext

        request = factory.get("/")
        return RequestContext(request, context_dict or {})

    return _get_context


@pytest.fixture
def sample_products(db):
    """Create sample products for integration testing."""
    from example.models import Category, Product

    # Create category
    category = Category.objects.create(
        name="Test Category",
        slug="test-category",
        description="Category for testing",
    )

    # Create 3 test products
    Product.objects.create(
        name="Product 1",
        slug="product-1",
        category=category,
        description="Description for product 1",
        short_description="Short desc 1",
        price=10.00,
        stock=10,
        status="published",
        sku="TEST001",
    )
    Product.objects.create(
        name="Product 2",
        slug="product-2",
        category=category,
        description="Description for product 2",
        short_description="Short desc 2",
        price=20.00,
        stock=10,
        status="published",
        sku="TEST002",
    )
    Product.objects.create(
        name="Product 3",
        slug="product-3",
        category=category,
        description="Description for product 3",
        short_description="Short desc 3",
        price=30.00,
        stock=10,
        status="published",
        sku="TEST003",
    )

    return Product.objects.all()
