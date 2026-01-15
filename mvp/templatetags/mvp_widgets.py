"""Template tags and filters for MVP navbar widgets."""

import hashlib

from django import template

register = template.Library()


@register.filter
def generate_initials(name):
    """Generate 1-2 character initials from a name.

    Args:
        name: Full name string (e.g., "John Doe", "Madonna", "José García")

    Returns:
        String of 1-2 uppercase letters representing initials

    Examples:
        >>> generate_initials("John Doe")
        'JD'
        >>> generate_initials("Madonna")
        'MA'
        >>> generate_initials("")
        'U'
        >>> generate_initials("O'Brien-Smith")
        'OS'
    """
    if not name or not name.strip():
        return "U"  # Unknown/User fallback

    # Remove special characters and extra whitespace
    clean_name = "".join(c for c in name if c.isalnum() or c.isspace())
    parts = clean_name.strip().split()

    if not parts:
        return "U"

    if len(parts) == 1:
        # Single name: use first 2 letters
        single = parts[0].upper()
        return single[:2] if len(single) >= 2 else single[0]

    # Multiple names: first letter of first and last name
    return (parts[0][0] + parts[-1][0]).upper()


@register.filter
def avatar_color(name):
    """Generate consistent color class for avatar based on name.

    Uses hash of name to deterministically pick from Bootstrap color palette.

    Args:
        name: Name string to generate color for

    Returns:
        Bootstrap background color class (e.g., 'bg-primary', 'bg-success')
    """
    if not name:
        name = "default"

    # Hash the name to get consistent color
    hash_value = int(hashlib.md5(name.encode()).hexdigest(), 16)

    # Bootstrap color palette for avatars
    colors = [
        "primary",
        "secondary",
        "success",
        "danger",
        "warning",
        "info",
    ]

    return f"text-bg-{colors[hash_value % len(colors)]}"
