"""
Tests for User Profile Widget (User Story 1).

Tests follow django-cotton patterns and verify:
- User widget rendering with name and avatar
- Initials fallback when no avatar
- Avatar fallback on broken image
- Responsive behavior (name hidden on mobile)
- Dropdown structure (header, body slot, footer)
"""

from django_cotton import render_component


class TestUserWidgetRendering:
    """Test user widget component rendering."""

    def test_user_widget_renders_with_name_and_avatar(self, rf):
        """User widget should render with user name and avatar image."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "John Doe",
                "image_url": "https://example.com/avatar.jpg",
            },
        )

        # Check widget structure
        assert 'class="nav-item dropdown"' in html
        assert 'aria-expanded="false"' in html

        # Check avatar with image
        assert "<img" in html
        assert 'src="https://example.com/avatar.jpg"' in html
        assert 'alt="John Doe"' in html

        # Check name display
        assert "John Doe" in html

    def test_user_widget_shows_initials_without_image(self, rf):
        """User widget should show initials when no avatar image provided."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "Jane Smith",
            },
        )

        # Check initials generated
        assert "JS" in html

        # Check no img tag
        assert "<img" not in html

    def test_avatar_fallback_on_broken_image(self, rf):
        """Avatar should handle broken image URLs gracefully."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "Bob Wilson",
                "image_url": "https://example.com/nonexistent.jpg",
            },
        )

        # Should have onerror handler for fallback
        assert "onerror" in html or "data-fallback-initials" in html

    def test_user_name_hidden_on_mobile(self, rf):
        """User name should have d-none d-md-inline class for mobile hiding."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "Alice Brown",
            },
        )

        # Check responsive classes for name
        assert "d-none" in html
        assert "d-md-inline" in html or "d-lg-inline" in html

    def test_dropdown_sections_structure(self, rf):
        """User widget dropdown should have header, body slot, and footer sections."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "Test User",
            },
        )

        # Check dropdown structure
        assert 'class="dropdown-menu' in html

        # Check header section exists
        assert "dropdown-header" in html or "dropdown-item-text" in html

        # Check footer section exists (typically with sign out link)
        assert "dropdown-divider" in html or "dropdown-footer" in html


class TestUserWidgetDropdownContent:
    """Test user widget dropdown content areas."""

    def test_dropdown_header_shows_user_info(self, rf):
        """Dropdown header should display user name and optional metadata."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "John Doe",
                "email": "john@example.com",
            },
        )

        # Header should show name
        assert "John Doe" in html

        # Email should be in dropdown if provided
        if "email" in html:
            assert "john@example.com" in html

    def test_dropdown_footer_has_sign_out(self, rf):
        """Dropdown footer should have sign out link."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "Test User",
            },
        )

        # Check for sign out or logout text
        assert "Sign out" in html or "Logout" in html or "Log out" in html


class TestUserWidgetAccessibility:
    """Test user widget accessibility features."""

    def test_widget_has_aria_label(self, rf):
        """User widget should have descriptive aria-label."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "John Doe",
            },
        )

        # Check for aria-label or aria-labelledby
        assert 'aria-label="User menu"' in html or "aria-labelledby=" in html

    def test_avatar_has_alt_text(self, rf):
        """Avatar image should have meaningful alt text."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/user",
            {
                "name": "Jane Smith",
                "image_url": "https://example.com/avatar.jpg",
            },
        )

        # Avatar should have alt attribute with user name
        assert 'alt="Jane Smith"' in html
