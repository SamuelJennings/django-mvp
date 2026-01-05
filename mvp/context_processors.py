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
                'breakpoint': 'lg',  # Show navbar menu at this breakpoint (navbar-only mode only)
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
    - breakpoint: Breakpoint where navbar menu becomes visible ('sm', 'md', 'lg', 'xl', 'xxl')
                       Default: 'lg'
                       Note: Only applies when sidebar.show_at is False (navbar-only mode)
                             Navbar menu is never shown when sidebar is in-flow

    Examples:
    - Navbar-only layout with menu at lg breakpoint (default):
        'sidebar': {'show_at': False},
        'navbar': {'breakpoint': 'lg'}  # Menu shows from 992px+

    - Navbar-only with menu at md breakpoint (earlier):
        'sidebar': {'show_at': False},
        'navbar': {'breakpoint': 'md'}  # Menu shows from 768px+

    - Navbar-only without navbar menu (sidebar toggle only):
        'sidebar': {'show_at': False},
        'navbar': {'breakpoint': False}  # No navbar menu

    - Desktop sidebar, mobile navbar (traditional):
        'sidebar': {'show_at': 'lg', 'collapsible': True}
        # navbar.breakpoint is ignored - menu never shows when sidebar in-flow

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
    - Validates layout_mode is one of: 'navbar', 'sidebar', or 'both' (default: 'sidebar')
    - Provides default values per spec: navbar-only with sidebar.show_at=False,
      sidebar.collapsible=True, navbar.breakpoint="sm"
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
    VALID_LAYOUT_MODES = {"navbar", "sidebar", "both"}

    # Make a copy to avoid mutating settings
    processed = config.copy()

    # Validate and set layout_mode (default: navbar per FR-010)
    layout_mode = processed.get("layout_mode", "navbar")
    if layout_mode not in VALID_LAYOUT_MODES:
        logger.warning(
            f"Invalid layout_mode: '{layout_mode}'. " f"Must be one of {VALID_LAYOUT_MODES}. Defaulting to 'navbar'."
        )
        layout_mode = "navbar"
    processed["layout_mode"] = layout_mode

    # Provide default values for all top-level keys per spec
    processed.setdefault("brand", {"text": "Django MVP"})
    processed.setdefault("actions", [])

    # Get or initialize sidebar and navbar configs with defaults
    sidebar_config = processed.setdefault("sidebar", {}).copy()
    navbar_config = processed.setdefault("navbar", {}).copy()

    # Apply sidebar defaults (navbar-only mode by default)
    sidebar_config.setdefault("breakpoint", False)
    sidebar_config.setdefault("collapsible", True)
    sidebar_config.setdefault("width", "260px")

    # Apply navbar defaults
    navbar_config.setdefault("fixed", False)
    navbar_config.setdefault("border", False)
    navbar_config.setdefault("breakpoint", "sm")  # Breakpoint for desktop vs mobile navbar style

    # Validate sidebar.breakpoint if it's a string
    sidebar_breakpoint = sidebar_config["breakpoint"]
    if isinstance(sidebar_breakpoint, str) and sidebar_breakpoint not in VALID_BREAKPOINTS:
        logger.warning(
            f"Invalid sidebar.breakpoint value: '{sidebar_breakpoint}'. "
            f"Must be one of {VALID_BREAKPOINTS} or False/None. Falling back to False."
        )
        sidebar_config["breakpoint"] = False

    # Get and validate navbar breakpoint
    navbar_breakpoint = navbar_config["breakpoint"]

    # Validate breakpoint if it's a string
    if isinstance(navbar_breakpoint, str) and navbar_breakpoint not in VALID_BREAKPOINTS:
        logger.warning(
            f"Invalid navbar.breakpoint value: '{navbar_breakpoint}'. "
            f"Must be one of {VALID_BREAKPOINTS}. Defaulting to 'sm'."
        )
        navbar_breakpoint = "sm"
        navbar_config["breakpoint"] = navbar_breakpoint

    # Enforce layout_mode rules for navbar.breakpoint
    # In sidebar-only mode, navbar should never show desktop menu (only hamburger toggle)
    if layout_mode == "sidebar" and sidebar_config["breakpoint"]:
        if navbar_config["breakpoint"]:
            logger.info(
                f"Sidebar-only mode with sidebar.breakpoint={sidebar_config['breakpoint']} "
                "enforces navbar.breakpoint=False (navbar shows hamburger only, no desktop menu)."
            )
        navbar_config["breakpoint"] = False

    # In navbar-only mode, sidebar is always offcanvas (sidebar.breakpoint must be False)
    if layout_mode == "navbar":
        if sidebar_config["breakpoint"]:
            logger.info(
                f"Navbar-only mode enforces sidebar.breakpoint=False "
                f"(was {sidebar_config['breakpoint']}). Sidebar is always offcanvas."
            )
        sidebar_config["breakpoint"] = False

    # Update processed config with validated values
    processed["sidebar"] = sidebar_config
    processed["navbar"] = navbar_config

    return processed
