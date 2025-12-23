"""Context processors for django-mvp."""

import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def page_config(request):
    """Provide page configuration to all templates.

    This context processor makes the PAGE_CONFIG dictionary available
    in all templates, allowing centralized control of page-level
    settings and components.

    The PAGE_CONFIG dictionary can contain:
    - brand: Site branding configuration (text, image_light, image_dark, icon_light, icon_dark)
    - actions: List of action widgets for navigation (icon, text, href, target, id)
    - sidebar: Sidebar navigation configuration
    - navbar: Navbar configuration
    - Any other page-level configuration

    Example settings.py configuration:
        PAGE_CONFIG = {
            'brand': {
                'text': 'My Site',
                'image_light': 'img/logo-light.svg',  # Optional, resolved with static tag
                'image_dark': 'img/logo-dark.svg',    # Optional, resolved with static tag
                'icon_light': 'img/icon-light.svg',   # Optional favicon for light theme
                'icon_dark': 'img/icon-dark.svg',     # Optional favicon for dark theme
            },
            'sidebar': {
                'show_at': 'lg',      # Show sidebar in-flow at this breakpoint and above
                                      # Use False or None for navbar-only (always offcanvas)
                'collapsible': True,  # Whether sidebar can collapse to icons only
                'width': '280px',     # Optional custom width
            },
            'navbar': {
                'fixed': True,         # Stick navbar to top
                'border': True,        # Show bottom border
                'menu_visible_at': 'lg',  # Show navbar menu at this breakpoint (navbar-only mode only)
            },
            'actions': [
                {'icon': 'sun-fill', 'text': 'Toggle theme', 'href': '#', 'id': 'themeToggle'},
                {'icon': 'github', 'text': 'GitHub', 'href': 'https://github.com/...', 'target': '_blank'},
            ],
        }

    Sidebar configuration:
    - show_at: Breakpoint where sidebar becomes visible in-flow ('sm', 'md', 'lg', 'xl', 'xxl')
               Set to False/None for navbar-only mode (sidebar always offcanvas)
    - collapsible: Boolean, whether sidebar can collapse to icon-only mode (default: True)
    - width: Optional custom width (default: '260px')

    Navbar configuration:
    - fixed: Boolean, whether navbar sticks to top (default: False)
    - border: Boolean, whether to show bottom border (default: False)
    - menu_visible_at: Breakpoint where navbar menu becomes visible ('sm', 'md', 'lg', 'xl', 'xxl')
                       Default: 'lg'
                       Note: Only applies when sidebar.show_at is False (navbar-only mode)
                             Navbar menu is never shown when sidebar is in-flow

    Examples:
    - Navbar-only layout with menu at lg breakpoint (default):
        'sidebar': {'show_at': False},
        'navbar': {'menu_visible_at': 'lg'}  # Menu shows from 992px+

    - Navbar-only with menu at md breakpoint (earlier):
        'sidebar': {'show_at': False},
        'navbar': {'menu_visible_at': 'md'}  # Menu shows from 768px+

    - Navbar-only without navbar menu (sidebar toggle only):
        'sidebar': {'show_at': False},
        'navbar': {'menu_visible_at': False}  # No navbar menu

    - Desktop sidebar, mobile navbar (traditional):
        'sidebar': {'show_at': 'lg', 'collapsible': True}
        # navbar.menu_visible_at is ignored - menu never shows when sidebar in-flow

    - Always show sidebar (even on mobile):
        'sidebar': {'show_at': 'sm', 'collapsible': False}

    Brand configuration:
    - If brand is falsy or not provided, no branding section is shown
    - text: Brand name to display
    - image_light: Optional path to logo for light theme (resolved via static tag)
    - image_dark: Optional path to logo for dark theme (resolved via static tag)
    - icon_light: Optional path to favicon for light theme (resolved via static tag)
    - icon_dark: Optional path to favicon for dark theme (resolved via static tag)

    Returns:
        dict: Dictionary containing 'page_config' key with the configuration.
    """
    config = getattr(settings, "PAGE_CONFIG", {})
    processed_config = _process_page_config(config)
    return {
        "page_config": processed_config,
    }


def _process_page_config(config):
    """Process and validate page configuration.

    This function enforces business rules and validates configuration values:
    - Provides default values per spec: navbar-only with sidebar.show_at=False,
      sidebar.collapsible=True, navbar.menu_visible_at="sm"
    - Validates breakpoint values are valid Bootstrap breakpoints
    - Enforces that navbar menu only shows in navbar-only mode
    - Ensures sidebar and navbar settings are consistent
    - Validates brand, sidebar, navbar, and actions keys

    Args:
        config: Raw PAGE_CONFIG dictionary from settings

    Returns:
        dict: Processed configuration with validated and derived values
    """
    VALID_BREAKPOINTS = {"sm", "md", "lg", "xl", "xxl"}

    # Make a copy to avoid mutating settings
    processed = config.copy()

    # Provide default values for all top-level keys per spec
    processed.setdefault("brand", {"text": "Django MVP"})
    processed.setdefault("actions", [])

    # Get or initialize sidebar and navbar configs with defaults
    sidebar_config = processed.setdefault("sidebar", {}).copy()
    navbar_config = processed.setdefault("navbar", {}).copy()

    # Apply sidebar defaults (navbar-only mode by default)
    sidebar_config.setdefault("show_at", False)
    sidebar_config.setdefault("collapsible", True)
    sidebar_config.setdefault("width", "260px")

    # Apply navbar defaults
    navbar_config.setdefault("fixed", False)
    navbar_config.setdefault("border", False)
    navbar_config.setdefault("menu_visible_at", "sm")  # Default per spec

    # Determine if we're in navbar-only mode
    sidebar_show_at = sidebar_config["show_at"]
    is_navbar_only = sidebar_show_at in {False, None}

    # Validate sidebar.show_at if it's a string
    if isinstance(sidebar_show_at, str) and sidebar_show_at not in VALID_BREAKPOINTS:
        logger.warning(
            f"Invalid sidebar.show_at value: '{sidebar_show_at}'. "
            f"Must be one of {VALID_BREAKPOINTS} or False/None. Falling back to False."
        )
        sidebar_config["show_at"] = False
        is_navbar_only = True

    # Get and validate navbar menu visibility breakpoint
    menu_visible_at = navbar_config["menu_visible_at"]

    # Validate breakpoint if it's a string
    if isinstance(menu_visible_at, str) and menu_visible_at not in VALID_BREAKPOINTS:
        logger.warning(
            f"Invalid navbar.menu_visible_at value: '{menu_visible_at}'. "
            f"Must be one of {VALID_BREAKPOINTS} or False/None. Defaulting to 'sm'."
        )
        menu_visible_at = "sm"

    # ENFORCEMENT: navbar menu can ONLY be visible in navbar-only mode
    # If sidebar is ever in-flow, navbar menu should never show
    if is_navbar_only and menu_visible_at not in {False, None}:
        # In navbar-only mode, use the configured breakpoint
        navbar_config["menu_visible_at"] = menu_visible_at
    else:
        # When sidebar is in-flow at any breakpoint, navbar menu is always hidden
        navbar_config["menu_visible_at"] = False

    # Update processed config with validated values
    processed["sidebar"] = sidebar_config
    processed["navbar"] = navbar_config

    return processed
