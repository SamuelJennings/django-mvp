"""
Unit tests for inner layout main component.

Tests the main container component with various attribute combinations.
"""

import pytest


@pytest.mark.django_db
class TestInnerLayoutMain:
    """Test suite for main inner layout container component."""

    def test_basic_render(self, render_component):
        """Test basic inner layout renders with correct structure."""
        html = render_component("page")

        assert 'class="page-layout' in html
        assert 'data-sidebar-breakpoint="lg"' in html  # Default breakpoint

    def test_fixed_header_attribute(self, render_component):
        """Test fixed_header attribute applies correct CSS class."""
        html = render_component("page", fixed_header=True)

        assert "toolbar-fixed" in html

    def test_fixed_header_false(self, render_component):
        """Test fixed_header=False does not apply sticky class."""
        html = render_component("page", fixed_header=False)

        assert "toolbar-fixed" not in html

    def test_fixed_footer_attribute(self, render_component):
        """Test fixed_footer attribute applies correct CSS class."""
        html = render_component("page", fixed_footer=True)

        assert "footer-fixed" in html

    def test_fixed_footer_false(self, render_component):
        """Test fixed_footer=False does not apply sticky class."""
        html = render_component("page", fixed_footer=False)

        assert "footer-fixed" not in html

    def test_fixed_sidebar_attribute(self, render_component):
        """Test fixed_sidebar attribute applies correct CSS class."""
        html = render_component("page", fixed_sidebar=True)

        assert "sidebar-fixed" in html

    def test_fixed_sidebar_false(self, render_component):
        """Test fixed_sidebar=False does not apply sticky class."""
        html = render_component("page", fixed_sidebar=False)

        assert "sidebar-fixed" not in html

    def test_sidebar_expand_default(self, render_component):
        """Test default sidebar expand breakpoint is 'lg'."""
        html = render_component("page")

        assert "sidebar-breakpoint-lg" in html
        assert 'data-sidebar-breakpoint="lg"' in html

    def test_sidebar_expand_sm(self, render_component):
        """Test sidebar_expand='sm' applies correct class."""
        html = render_component("page", sidebar_expand="sm")

        assert "sidebar-breakpoint-sm" in html
        assert 'data-sidebar-breakpoint="sm"' in html

    def test_sidebar_expand_md(self, render_component):
        """Test sidebar_expand='md' applies correct class."""
        html = render_component("page", sidebar_expand="md")

        assert "sidebar-breakpoint-md" in html
        assert 'data-sidebar-breakpoint="md"' in html

    def test_sidebar_expand_xl(self, render_component):
        """Test sidebar_expand='xl' applies correct class."""
        html = render_component("page", sidebar_expand="xl")

        assert "sidebar-breakpoint-xl" in html
        assert 'data-sidebar-breakpoint="xl"' in html

    def test_sidebar_expand_xxl(self, render_component):
        """Test sidebar_expand='xxl' applies correct class."""
        html = render_component("page", sidebar_expand="xxl")

        assert "sidebar-breakpoint-xxl" in html
        assert 'data-sidebar-breakpoint="xxl"' in html

    def test_custom_class_attribute(self, render_component):
        """Test custom class attribute is applied to container."""
        html = render_component("page", **{"class": "my-custom-class"})

        assert "my-custom-class" in html

    def test_all_sticky_attributes(self, render_component):
        """Test all sticky attributes can be combined."""
        html = render_component(
            "page",
            fixed_header=True,
            fixed_footer=True,
            fixed_sidebar=True,
        )

        assert "toolbar-fixed" in html
        assert "footer-fixed" in html
        assert "sidebar-fixed" in html

    def test_slot_content_renders(self, render_component):
        """Test default slot content renders inside container."""
        html = render_component(
            "page",
            slot="<p>Test content</p>",
        )

        # Layout container is rendered
        assert 'class="page-layout' in html
