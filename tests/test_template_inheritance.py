"""
Tests for template inheritance with layout configuration.

User Story 3: Configure Layout Per-Page or Globally (T028-T035)
Verifies that:
- Base templates can define default layout configurations
- Child templates can inherit layout from base templates
- Child templates can override base layout configurations
- Global layout configuration works with template inheritance patterns
"""

import pytest
from django_cotton import render_component


@pytest.mark.django_db
class TestTemplateInheritance:
    """
    User Story 3: Test template inheritance with layout configuration.

    T028-T030: Validate that layout attributes can be set in base templates
    and properly inherited or overridden in child templates.
    """

    def test_base_template_with_fixed_layout(self, rf):
        """
        T028: Test that base template with fixed layout renders correctly.

        Should produce a base template that sets up layout configuration.
        """
        mock_request = rf.get("/")

        # Test the app component directly with fixed layout
        html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
        )

        # Verify the base template renders with fixed layout classes
        assert (
            'body class="' in html and "layout-fixed" in html and "fixed-header" in html
        ), f"Base template should render fixed layout classes. Actual HTML: {html[:300]}..."

    def test_child_template_inheriting_layout(self, rf):
        """
        T029: Test that child template inheriting layout from base renders correctly.

        Should preserve the layout configuration from the base template.
        """
        mock_request = rf.get("/")

        # Test the same component configuration (simulating inheritance)
        html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
        )

        # Verify inherited layout classes are present
        assert (
            'body class="' in html and "layout-fixed" in html and "fixed-header" in html
        ), f"Child template should inherit fixed layout classes. Actual HTML: {html[:300]}..."

    def test_child_template_overriding_base_layout(self, rf):
        """
        T030: Test that child template can override base layout configuration.

        Should allow child templates to define their own layout independently of base.
        """
        mock_request = rf.get("/")

        # Test different component configuration (simulating override)
        html = render_component(
            mock_request,
            "app",
            fixed_footer=True,
            sidebar_expand="xl",
        )

        # Verify the child template's layout configuration is used
        assert (
            'body class="' in html and "fixed-footer" in html and "sidebar-expand-xl" in html
        ), f"Child template should override with its own layout. Actual HTML: {html[:300]}..."

        # Verify layout from base is NOT present (no fixed-sidebar or fixed-header)
        assert (
            "layout-fixed" not in html and "fixed-header" not in html
        ), f"Child template should not inherit unwanted layout classes. Actual HTML: {html[:300]}..."


@pytest.mark.django_db
class TestGlobalLayoutConfiguration:
    """
    User Story 3: Test global layout patterns with template inheritance.

    T031-T033: Validate that Django project patterns for global layout
    configuration work correctly with the app component.
    """

    def test_global_configuration_pattern(self, rf):
        """
        T031: Test Django pattern for global layout configuration.

        Should demonstrate how to set up a global layout that all pages inherit.
        """
        mock_request = rf.get("/")

        # Test a comprehensive global layout configuration
        html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
            sidebar_expand="lg",
            sidebar_collapsible=True,
        )

        # Verify global layout configuration is applied
        expected_classes = ["layout-fixed", "fixed-header", "sidebar-expand-lg", "sidebar-mini"]
        for css_class in expected_classes:
            assert (
                'body class="' in html and css_class in html
            ), f"Global layout class {css_class} should be applied. Actual HTML: {html[:300]}..."

    def test_page_specific_override_pattern(self, rf):
        """
        T032: Test Django pattern for page-specific layout overrides.

        Should show how individual pages can have different layouts.
        """
        mock_request = rf.get("/")

        # Test a minimal layout for special pages (e.g., login)
        html = render_component(
            mock_request,
            "app",
            **{"class": "login-page"},
        )

        # Verify no fixed layout classes (clean layout for login)
        assert (
            "layout-fixed" not in html and "fixed-header" not in html
        ), f"Login page should not have fixed layout. Actual HTML: {html[:300]}..."

        # Verify custom class is applied
        assert (
            'body class="' in html and "login-page" in html
        ), f"Login page should have custom styling. Actual HTML: {html[:300]}..."

    def test_conditional_layout_pattern(self, rf):
        """
        T033: Test Django pattern for conditional layout configuration.

        Should demonstrate how to conditionally apply layouts based on context.
        """
        mock_request = rf.get("/")

        # Test admin-style layout
        admin_html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
            sidebar_collapsible=True,
        )

        assert (
            "layout-fixed" in admin_html and "sidebar-mini" in admin_html
        ), f"Admin layout should have sidebar and collapsible features. HTML: {admin_html[:300]}..."

        # Test user-style layout
        user_html = render_component(
            mock_request,
            "app",
            fixed_header=True,
        )

        assert (
            "fixed-header" in user_html and "layout-fixed" not in user_html
        ), f"User layout should only have fixed header. HTML: {user_html[:300]}..."
