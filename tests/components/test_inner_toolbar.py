"""
Unit tests for inner layout toolbar component.

Tests the toolbar component and its widget subcomponent.
"""

import pytest


@pytest.mark.django_db
class TestInnerToolbar:
    """Test suite for inner layout toolbar component."""

    def test_basic_toolbar_render(self, render_component):
        """Test basic toolbar renders with correct structure."""
        html = render_component("page.toolbar")

        assert 'class="mvp-header' in html
        assert 'role="banner"' in html
        assert 'aria-label="Page toolbar"' in html

    def test_toolbar_start_slot(self, render_component):
        """Test toolbar start slot renders content."""
        html = render_component(
            "page.toolbar",
            slot="<h2>Page Title</h2>",
        )

        # Content is rendered
        assert '<h2>Page Title</h2>' in html

    def test_toolbar_end_slot(self, render_component):
        """Test toolbar end slot renders content."""
        html = render_component(
            "page.toolbar",
            end="<button>Action</button>",
        )

        # Content appears (escaped) in the end slot
        assert "Action" in html

    def test_toolbar_custom_class(self, render_component):
        """Test custom class attribute is applied."""
        html = render_component("page.toolbar", **{"class": "custom-toolbar"})

        assert "custom-toolbar" in html

    def test_toolbar_compact_mode(self, render_component):
        """Test compact mode applies correct class."""
        html = render_component("page.toolbar", **{"class": "compact"})

        assert "compact" in html

    def test_toolbar_relaxed_mode(self, render_component):
        """Test relaxed mode applies correct class."""
        html = render_component("page.toolbar", **{"class": "relaxed"})

        assert "relaxed" in html


@pytest.mark.django_db
class TestInnerToolbarWidget:
    """Test suite for inner layout toolbar widget (toggle button)."""

    def test_widget_basic_render(self, render_component):
        """Test widget renders with correct structure."""
        html = render_component("page.toolbar.sidebar_widget")

        assert 'data-action="toggle-sidebar"' in html
        assert 'role="button"' in html or 'type="button"' in html

    def test_widget_aria_attributes(self, render_component):
        """Test widget has correct ARIA attributes."""
        html = render_component("page.toolbar.sidebar_widget")

        assert 'aria-expanded="true"' in html
        assert 'aria-label="Toggle sidebar"' in html or 'aria-controls="page-sidebar"' in html

    def test_widget_icon_rendering(self, render_component):
        """Test widget renders toggle icons."""
        html = render_component("page.toolbar.widget")

        # Should have icon element (bi classes from Bootstrap Icons)
        assert "bi-arrow" in html or '<i class="bi' in html

    def test_widget_custom_class(self, render_component):
        """Test custom class attribute is applied to widget."""
        html = render_component("page.toolbar.widget", **{"class": "custom-widget"})

        assert "custom-widget" in html
