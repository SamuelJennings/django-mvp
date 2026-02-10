"""
Unit tests for inner layout sidebar component.

Tests the sidebar component rendering and collapsed state.
"""

import pytest


@pytest.mark.django_db
class TestInnerSidebar:
    """Test suite for inner layout sidebar component."""

    def test_basic_sidebar_render(self, cotton_render):
        """Test basic sidebar renders with correct structure."""
        html = cotton_render("page.sidebar")

        assert 'class="mvp-sidebar' in html
        assert 'role="complementary"' in html
        assert 'aria-label="Sidebar content"' in html

    def test_sidebar_slot_content(self, cotton_render):
        """Test sidebar slot renders content."""
        html = cotton_render(
            "page.sidebar",
            slot="<div>Sidebar content</div>",
        )

        assert "<div>Sidebar content</div>" in html

    def test_sidebar_collapsed_attribute_false(self, cotton_render):
        """Test collapsed=False does not add collapsed class."""
        html = cotton_render("page.sidebar", collapsed=False)

        assert 'class="mvp-sidebar' in html
        # Should not have collapsed class
        assert 'class="mvp-sidebar collapsed' not in html

    def test_sidebar_collapsed_attribute_true(self, cotton_render):
        """Test collapsed=True adds collapsed class."""
        html = cotton_render("page.sidebar", collapsed=True)

        assert "collapsed" in html

    def test_sidebar_custom_class(self, cotton_render):
        """Test custom class attribute is applied."""
        html = cotton_render("page.sidebar", **{"class": "custom-sidebar"})

        assert "custom-sidebar" in html

    def test_sidebar_default_styling(self, cotton_render):
        """Test sidebar has correct default styling classes."""
        html = cotton_render("page.sidebar")

        # Check for mvp-sidebar class
        assert "mvp-sidebar" in html

    def test_sidebar_with_complex_content(self, cotton_render):
        """Test sidebar renders complex nested content."""
        complex_content = """
            <div class="p-3">
                <h6>Filter Options</h6>
                <form>
                    <input type="text" placeholder="Search">
                </form>
            </div>
        """
        html = cotton_render("page.sidebar", slot=complex_content)

        assert "Filter Options" in html
        assert '<input type="text"' in html
        assert 'class="mvp-sidebar' in html
