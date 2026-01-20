"""
Integration tests for inner layout component configuration.

Tests that responsive breakpoints can be configured independently per page.
"""

import pytest
from django.template import Context, Template
from django_cotton.compiler_regex import CottonCompiler


class TestPageLayoutMultiPageConfigurations:
    """Test template-driven configuration across multiple page contexts."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.compiler = CottonCompiler()

    def render_template(self, template_string, context=None):
        """Helper method to render a template string with context."""
        if context is None:
            context = {}
        template = self.compiler.process(template_string)
        return Template(template).render(Context(context))

    def test_breakpoint_per_page_configuration(self):
        """Test that responsive breakpoints can be configured independently per page."""
        # Page 1: md breakpoint
        page1_template = """
        <c-page sidebar_expand="md">
            <c-slot name="sidebar">Sidebar</c-slot>
            <p>Content</p>
        </c-page>
        """
        page1_result = self.render_template(page1_template)

        # Page 2: xl breakpoint
        page2_template = """
        <c-page sidebar_expand="xl">
            <c-slot name="sidebar">Sidebar</c-slot>
            <p>Content</p>
        </c-page>
        """
        page2_result = self.render_template(page2_template)

        # Verify each page has correct breakpoint class
        assert "sidebar-breakpoint-md" in page1_result
        assert "sidebar-breakpoint-xl" in page2_result
        # Verify they don't cross-contaminate
        assert "sidebar-breakpoint-xl" not in page1_result
        assert "sidebar-breakpoint-md" not in page2_result
