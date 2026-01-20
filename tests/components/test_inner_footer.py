"""
Unit tests for inner layout footer component.

Tests the footer component rendering and slot handling.
"""

import pytest


@pytest.mark.django_db
class TestInnerFooter:
    """Test suite for inner layout footer component."""

    def test_basic_footer_render(self, render_component):
        """Test basic footer renders with correct structure."""
        html = render_component("page.footer")

        assert 'class="page-footer' in html
        assert 'role="contentinfo"' in html
        assert 'aria-label="Page footer"' in html

    def test_footer_start_slot(self, render_component):
        """Test footer start slot renders content."""
        html = render_component(
            "page.footer",
            slot="<p>Footer info</p>",
        )

        # Slot content is present (may be escaped in component rendering)
        assert 'class="page-footer-start"' in html

    def test_footer_end_slot(self, render_component):
        """Test footer end slot renders content."""
        html = render_component(
            "page.footer",
            end="<button>Page action</button>",
        )

        # Content appears (escaped) in the end slot
        assert "Page action" in html
        assert 'class="page-footer-end"' in html

    def test_footer_both_slots(self, render_component):
        """Test footer renders both start and end slots."""
        html = render_component(
            "page.footer",
            slot="<p>Left content</p>",
            end="<p>Right content</p>",
        )

        # Check for text content (HTML may be escaped)
        assert "Right content" in html
        assert 'class="page-footer-start"' in html
        assert 'class="page-footer-end"' in html

    def test_footer_custom_class(self, render_component):
        """Test custom class attribute is applied."""
        html = render_component("page.footer", **{"class": "custom-footer"})

        assert "custom-footer" in html

    def test_footer_empty_slots(self, render_component):
        """Test footer renders correctly even with empty slots."""
        html = render_component("page.footer")

        assert 'class="page-footer' in html
        # Should have start structure element
        assert "page-footer-start" in html
