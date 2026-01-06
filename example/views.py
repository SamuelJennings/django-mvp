"""
Demo views for testing AdminLTE layout configurations.

These views provide interactive forms for testing:
- Fixed properties (fixed_sidebar, fixed_header, fixed_footer)
- Responsive breakpoints (sidebar_expand)

Views use query parameters for stateless, shareable URL-based configuration.
"""

from django.shortcuts import render


def layout_fixed_demo(request):
    """
    Demo view for testing fixed layout properties.

    Query Parameters:
        fixed_sidebar (str): 'on' if checkbox is checked
        fixed_header (str): 'on' if checkbox is checked
        fixed_footer (str): 'on' if checkbox is checked

    Returns:
        Rendered template with checkbox form and layout demonstration
    """
    # Parse query parameters (checkboxes send 'on' when checked, absent when unchecked)
    fixed_sidebar = request.GET.get("fixed_sidebar") == "on"
    fixed_header = request.GET.get("fixed_header") == "on"
    fixed_footer = request.GET.get("fixed_footer") == "on"

    context = {
        "fixed_sidebar": fixed_sidebar,
        "fixed_header": fixed_header,
        "fixed_footer": fixed_footer,
    }

    return render(request, "example/layout_fixed.html", context)


def layout_responsive_demo(request):
    """
    Demo view for testing responsive sidebar breakpoints.

    Query Parameters:
        breakpoint (str): Bootstrap breakpoint (sm, md, lg, xl, xxl)
                         Defaults to 'lg' if not provided or invalid

    Returns:
        Rendered template with breakpoint dropdown and layout demonstration
    """
    # Valid Bootstrap 5 breakpoints
    valid_breakpoints = ["sm", "md", "lg", "xl", "xxl"]

    # Get breakpoint from query param, default to 'lg'
    sidebar_breakpoint = request.GET.get("breakpoint", "lg")

    # Validate breakpoint, fallback to 'lg' if invalid
    if sidebar_breakpoint not in valid_breakpoints:
        sidebar_breakpoint = "lg"

    context = {
        "breakpoint": sidebar_breakpoint,
        "breakpoints": valid_breakpoints,
    }

    return render(request, "example/layout_responsive.html", context)
