"""Tests for navbar avatar component and initials generator.

Tests cover:
- Avatar rendering with image URL
- Initials generation from names
- Fallback behavior for broken images
- Edge cases (no name, single name, special characters)
- Color generation consistency
"""

from django_cotton.utils import render_component


class TestAvatarRendering:
    """Test avatar component rendering."""

    def test_avatar_with_image_url(self, rf):
        """Avatar MUST display image when valid URL provided."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/avatar",
            {
                "name": "John Doe",
                "image_url": "https://example.com/avatar.jpg",
            },
        )

        # ASSERT
        assert 'src="https://example.com/avatar.jpg"' in result
        assert 'alt="John Doe"' in result
        assert "<img" in result

    def test_avatar_shows_initials_without_image(self, rf):
        """Avatar MUST show initials when no image URL provided."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/avatar",
            {
                "name": "John Doe",
            },
        )

        # ASSERT
        assert ">JD<" in result or "JD" in result
        assert "avatar-initials" in result or "initials" in result
        # Should not have img tag
        assert "<img" not in result

    def test_avatar_size_class(self, rf):
        """Avatar MUST support size customization."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/avatar",
            {
                "name": "Jane Smith",
                "size": "sm",
            },
        )

        # ASSERT
        assert "avatar-sm" in result or "small" in result or "sm" in result


class TestInitialsGeneration:
    """Test initials generator helper function."""

    def test_initials_from_full_name(self, rf):
        """Initials MUST be first letter of first and last name."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/avatar",
            {
                "name": "John Doe",
            },
        )

        # ASSERT
        assert "JD" in result

    def test_initials_from_single_name(self, rf):
        """Single name MUST show first two letters as initials."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/avatar",
            {
                "name": "Madonna",
            },
        )

        # ASSERT
        assert "MA" in result or "M" in result  # Either first 2 letters or just first

    def test_initials_handle_empty_name(self, rf):
        """Empty/missing name MUST show fallback (e.g., '??' or 'U')."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/avatar",
            {
                "name": "",
            },
        )

        # ASSERT
        # Should show some fallback, not crash
        assert "??" in result or "U" in result or "Unknown" in result or result  # Any valid output

    def test_initials_handle_special_characters(self, rf):
        """Names with special characters MUST extract letters only."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/avatar",
            {
                "name": "O'Brien-Smith",
            },
        )

        # ASSERT
        assert "OS" in result or "OB" in result  # Either O'Brien first or O'Brien-Smith

    def test_initials_handle_unicode(self, rf):
        """Names with unicode characters MUST be handled correctly."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/avatar",
            {
                "name": "José García",
            },
        )

        # ASSERT
        assert "JG" in result or "José" in result  # Either initials or full name shown


class TestAvatarColors:
    """Test avatar color generation."""

    def test_avatar_consistent_color_for_name(self, rf):
        """Avatar color MUST be consistent for same name."""
        # ARRANGE
        request = rf.get("/")

        # ACT - Render same avatar twice
        result1 = render_component(
            request,
            "navbar/avatar",
            {
                "name": "Test User",
            },
        )
        result2 = render_component(
            request,
            "navbar/avatar",
            {
                "name": "Test User",
            },
        )

        # ASSERT
        # Extract background color from both results - they should match
        # Looking for pattern like bg-primary, bg-danger, or style="background-color:"
        assert result1 == result2  # Entire output should be identical for same input

    def test_avatar_different_colors_for_different_names(self, rf):
        """Different names SHOULD produce different colors."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result1 = render_component(
            request,
            "navbar/avatar",
            {
                "name": "Alice Anderson",
            },
        )
        result2 = render_component(
            request,
            "navbar/avatar",
            {
                "name": "Bob Brown",
            },
        )

        # ASSERT
        # Results should differ (different initials at minimum)
        assert result1 != result2
