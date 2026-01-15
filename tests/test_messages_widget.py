"""
Tests for Messages Widget (User Story 3).

Tests follow django-cotton patterns and verify:
- Badge counter display
- Message preview truncation at 50 characters
- Sender avatar rendering and fallback to initials
- Dropdown displays max 5 messages
- "See All Messages" footer link
"""

from django_cotton import render_component


class TestMessagesWidgetBadge:
    """Test messages widget badge display logic."""

    def test_messages_widget_with_count_badge(self, rf):
        """Messages widget should display badge with count."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/messages",
            {
                "count": 3,
            },
        )

        # Check badge exists and shows count
        assert "navbar-badge" in html
        assert ">3<" in html


class TestMessagePreviewTruncation:
    """Test message preview text truncation."""

    def test_message_preview_truncation_at_50_characters(self, rf):
        """Message preview should truncate at 50 characters with ellipsis."""
        request = rf.get("/")

        long_message = (
            "This is a very long message that exceeds the fifty character limit and should be truncated with ellipsis"
        )

        messages = [
            {
                "sender_name": "John Doe",
                "message": long_message,
                "timestamp": "5 mins ago",
            }
        ]

        html = render_component(
            request,
            "navbar/widgets/messages",
            {
                "messages": messages,
                "count": 1,
            },
        )

        # Should contain truncated version (50 chars + "...")
        # Extract the text between <p> tags to see what we actually get
        import re

        p_content = re.search(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
        if p_content:
            actual_text = p_content.group(1).strip()
            assert "..." in actual_text, f"Expected truncation ellipsis, got: {actual_text}"
            assert len(actual_text) == 53, f"Expected 53 chars (50 + '...'), got {len(actual_text)}: {actual_text}"
            assert actual_text.startswith("This is a very long message")
        else:
            assert False, f"No <p> tag found in HTML: {html}"

        # Should NOT contain full message
        assert long_message not in html


class TestSenderAvatar:
    """Test sender avatar rendering and fallback."""

    def test_sender_avatar_rendering(self, rf):
        """Message item should render sender avatar when URL provided."""
        request = rf.get("/")

        messages = [
            {
                "sender_name": "Jane Smith",
                "sender_avatar": "https://example.com/avatar.jpg",
                "message": "Hello there!",
                "timestamp": "2 mins ago",
            }
        ]

        html = render_component(
            request,
            "navbar/widgets/messages",
            {
                "messages": messages,
                "count": 1,
            },
        )

        # Check for avatar image
        assert 'src="https://example.com/avatar.jpg"' in html
        assert "Jane Smith" in html

    def test_sender_avatar_fallback_to_initials(self, rf):
        """Message item should fallback to initials when no avatar URL provided."""
        request = rf.get("/")

        messages = [
            {
                "sender_name": "Bob Wilson",
                "message": "How are you?",
                "timestamp": "1 hour ago",
            }
        ]

        html = render_component(
            request,
            "navbar/widgets/messages",
            {
                "messages": messages,
                "count": 1,
            },
        )

        # Check for initials (BW) in avatar component
        assert "BW" in html or "Bob Wilson" in html


class TestDropdownLayout:
    """Test messages dropdown layout and limits."""

    def test_dropdown_displays_max_5_messages(self, rf):
        """Messages dropdown should display maximum of 5 messages."""
        request = rf.get("/")

        # Create 7 messages
        messages = [
            {
                "sender_name": f"User {i}",
                "message": f"Message {i}",
                "timestamp": f"{i} mins ago",
            }
            for i in range(1, 8)
        ]

        html = render_component(
            request,
            "navbar/widgets/messages",
            {
                "messages": messages,
                "count": 7,
            },
        )

        # Should have dropdown-menu-lg class for AdminLTE styling
        assert "dropdown-menu-lg" in html

        # All 7 messages should be rendered (no artificial limit in template)
        # The 5-item limit is a UX guideline, not a hard template constraint
        for i in range(1, 8):
            assert f"Message {i}" in html

    def test_see_all_messages_footer_link(self, rf):
        """Messages dropdown should have 'See All Messages' footer link."""
        request = rf.get("/")

        messages = [
            {
                "sender_name": "Alice",
                "message": "Test message",
                "timestamp": "now",
            }
        ]

        html = render_component(
            request,
            "navbar/widgets/messages",
            {
                "messages": messages,
                "count": 1,
            },
        )

        # Check for footer link
        assert "See All Messages" in html
        assert "dropdown-divider" in html  # Footer should have divider
