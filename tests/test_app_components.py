"""
Tests for app layout components (wrapper, header, sidebar, main, footer).

These tests verify that each component:
- Renders with correct HTML structure
- Applies CSS classes correctly
- Handles c-vars appropriately
- Renders slots correctly

Uses django_cotton.render_component() with pytest-django's rf fixture.
"""

import pytest
from django_cotton import render_component


@pytest.fixture
def mock_request(rf):
    """Fixture providing a mock HTTP request using pytest-django's rf fixture."""
    return rf.get("/")


@pytest.mark.django_db
class TestWrapperComponent:
    """Tests for app/index.html component (the app wrapper)."""

    def test_renders_basic_structure(self, mock_request):
        """Wrapper renders with default .app-wrapper div."""
        html = render_component(mock_request, "app")
        assert 'class="app-wrapper' in html
        assert "</div>" in html

    def test_applies_body_class(self, mock_request):
        """Wrapper applies custom body_class (via class attribute)."""
        html = render_component(mock_request, "app", **{"class": "custom-layout"})
        assert 'class="app-wrapper' in html
        assert "custom-layout" in html

    def test_applies_sidebar_expand(self, mock_request):
        """Wrapper applies sidebar_expand class."""
        html = render_component(mock_request, "app", sidebar_expand="lg")
        assert "sidebar-expand-lg" in html

    def test_applies_fixed_sidebar(self, mock_request):
        """Wrapper applies layout-fixed class when fixed_sidebar is True."""
        html = render_component(mock_request, "app", fixed_sidebar=True)
        assert "layout-fixed" in html


@pytest.mark.django_db
class TestHeaderComponent:
    """Tests for app/header/ subdirectory components."""

    def test_toggle_renders_basic_structure(self, mock_request):
        """Header toggle renders nav-item with sidebar toggle button."""
        html = render_component(mock_request, "app/header/toggle")
        assert '<li class="nav-item">' in html
        assert 'data-lte-toggle="sidebar"' in html
        assert '<i class="bi bi-list"></i>' in html

    def test_toggle_applies_class(self, mock_request):
        """Header toggle applies custom class to nav-link."""
        html = render_component(mock_request, "app/header/toggle", **{"class": "custom-toggle"})
        assert "custom-toggle" in html

    def test_header_renders_basic_structure(self, mock_request):
        """Header index renders with app-header nav element."""
        html = render_component(mock_request, "app/header")
        assert 'class="app-header navbar navbar-expand bg-body' in html
        # Should include toggle component
        assert 'data-lte-toggle="sidebar"' in html

    def test_header_applies_class(self, mock_request):
        """Header index applies custom class."""
        html = render_component(mock_request, "app/header", **{"class": "navbar-dark"})
        assert "navbar-dark" in html

    def test_header_applies_container_class(self, mock_request):
        """Header index applies custom container_class."""
        html = render_component(mock_request, "app/header", container_class="container")
        assert '<div class="container">' in html

    def test_header_renders_left_and_right_slots(self, mock_request):
        """Header index renders both navbar-nav sections for left/right slots."""
        html = render_component(mock_request, "app/header")
        assert '<ul class="navbar-nav">' in html
        assert '<ul class="navbar-nav ms-auto">' in html


@pytest.mark.django_db
class TestFooterComponent:
    """Tests for app/footer.html component."""

    def test_renders_basic_structure(self, mock_request):
        """Footer renders with app-footer element."""
        html = render_component(mock_request, "app/footer")
        assert 'class="app-footer' in html

    def test_applies_default_text(self, mock_request):
        """Footer displays default copyright text."""
        html = render_component(mock_request, "app/footer")
        # HTML entities may be escaped
        assert "Copyright" in html and "2026" in html

    def test_applies_custom_text(self, mock_request):
        """Footer displays custom text when provided."""
        html = render_component(mock_request, "app/footer", text="© 2026 Custom Company")
        assert "© 2026 Custom Company" in html

    def test_applies_class(self, mock_request):
        """Footer applies custom class."""
        html = render_component(mock_request, "app/footer", **{"class": "mt-5"})
        assert 'class="app-footer mt-5"' in html


@pytest.mark.django_db
class TestSidebarComponent:
    """Tests for app/sidebar/ subdirectory components."""

    def test_sidebar_renders_basic_structure(self, mock_request):
        """Sidebar index renders with app-sidebar aside element."""
        html = render_component(mock_request, "app/sidebar")
        assert 'class="app-sidebar' in html
        assert "data-bs-theme=" in html

    def test_sidebar_applies_brand_text(self, mock_request):
        """Sidebar displays custom brand text."""
        html = render_component(mock_request, "app/sidebar", brand_text="My Custom App")
        assert "My Custom App" in html

    def test_sidebar_applies_brand_logo(self, mock_request):
        """Sidebar includes brand logo when provided."""
        html = render_component(mock_request, "app/sidebar", brand_logo="/static/logo.png")
        assert 'src="/static/logo.png"' in html

    def test_sidebar_applies_theme(self, mock_request):
        """Sidebar applies custom theme."""
        html = render_component(mock_request, "app/sidebar", theme="light")
        assert 'data-bs-theme="light"' in html

    def test_sidebar_applies_class(self, mock_request):
        """Sidebar applies custom class."""
        html = render_component(mock_request, "app/sidebar", **{"class": "custom-sidebar"})
        assert "custom-sidebar" in html


@pytest.mark.django_db
class TestMainComponent:
    """Tests for app/main/ subdirectory components."""

    def test_main_renders_basic_structure(self, mock_request):
        """Main index renders with app-main main element."""
        html = render_component(mock_request, "app/main")
        assert '<main class="app-main">' in html
        assert '<div class="app-content">' in html

    def test_main_renders_content_header_by_default(self, mock_request):
        """Main renders content header by default."""
        html = render_component(mock_request, "app/main")
        assert '<div class="app-content-header">' in html

    def test_main_hides_content_header_when_disabled(self, mock_request):
        """Main hides content header when show_header is False."""
        html = render_component(mock_request, "app/main", show_header="False")
        assert '<div class="app-content-header">' not in html

    def test_main_applies_container_class(self, mock_request):
        """Main applies custom container_class to content header."""
        html = render_component(mock_request, "app/main", container_class="container")
        assert '<div class="container">' in html


@pytest.mark.django_db
class TestEdgeCases:
    """Tests for edge cases as defined in spec.md."""

    def test_wrapper_with_missing_optional_cvars(self, mock_request):
        """Wrapper renders correctly with missing optional c-vars."""
        html = render_component(mock_request, "app/wrapper")
        # Should render with defaults
        assert 'class="app-wrapper' in html
        # Should not have optional modifiers when not specified
        assert "layout-fixed" not in html
        assert "custom" not in html

    def test_sidebar_without_logo(self, mock_request):
        """Sidebar renders correctly without brand_logo."""
        html = render_component(mock_request, "app/sidebar", brand_text="No Logo App", brand_logo="")
        assert "No Logo App" in html
        # Should not render img tag
        assert "<img" not in html

    def test_footer_with_empty_text(self, mock_request):
        """Footer uses default text when text c-var is empty."""
        html = render_component(mock_request, "app/footer", text="")
        # Empty text should still render structure
        assert 'class="app-footer' in html
