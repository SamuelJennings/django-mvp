"""Context processors for django-cotton-layouts."""

from django.conf import settings


def page_config(request):
    """Provide page configuration to all templates.

    This context processor makes the PAGE_CONFIG dictionary available
    in all templates, allowing centralized control of page-level
    settings and components.

    The PAGE_CONFIG dictionary can contain:
    - layout: Layout type ('sidebar', 'navbar', or 'both')
    - brand: Site branding configuration (text, image_light, image_dark, icon_light, icon_dark)
    - actions: List of action widgets for navigation (icon, text, href, target, id)
    - navigation: Navigation menu settings (sidebar and navbar configuration)
    - Any other page-level configuration

    Example settings.py configuration:
        PAGE_CONFIG = {
            'layout': 'sidebar',  # Layout type: 'sidebar', 'navbar', or 'both'
            'brand': {
                'text': 'My Site',
                'image_light': 'img/logo-light.svg',  # Optional, resolved with static tag
                'image_dark': 'img/logo-dark.svg',    # Optional, resolved with static tag
                'icon_light': 'img/icon-light.svg',   # Optional favicon for light theme
                'icon_dark': 'img/icon-dark.svg',     # Optional favicon for dark theme
            },
            'navigation': {
                'sidebar': {
                    'collapsible': True,  # Whether sidebar can collapse to icons only
                    'show_at': 'lg',      # BS5 breakpoint for sidebar visibility (sm, md, lg, xl, xxl)
                },
                # Set to False to disable sidebar: 'sidebar': False
            },
            'actions': [
                {'icon': 'sun-fill', 'text': 'Toggle theme', 'href': '#', 'id': 'themeToggle'},
                {'icon': 'github', 'text': 'GitHub', 'href': 'https://github.com/...', 'target': '_blank'},
                {'icon': 'question-circle', 'text': 'Support', 'href': '/support/'},
            ],
        }

    Layout configuration:
    - If not specified, defaults to 'sidebar'
    - 'sidebar': Sidebar always visible at sidebar.show_at and above; navbar only visible below sidebar.show_at
                 Use this for traditional sidebar-based layouts where the navbar serves as a mobile-only header
    - 'navbar': Navbar always visible at all screen sizes; sidebar only accessible via toggle (offcanvas)
                Use this for navbar-first layouts where sidebar is a secondary navigation drawer
    - 'both': Both sidebar and navbar visible simultaneously at sidebar.show_at and above
              Use this for complex layouts requiring both persistent sidebar and top navbar

    Note: Both components are always rendered in the DOM. The layout setting controls their
    visibility at different screen sizes using Bootstrap's responsive display utilities.

    Brand configuration:
    - If brand is falsy or not provided, no branding section is shown
    - text: Brand name to display
    - image_light: Optional path to logo for light theme (resolved via static tag)
    - image_dark: Optional path to logo for dark theme (resolved via static tag)
    - icon_light: Optional path to favicon for light theme (resolved via static tag)
    - icon_dark: Optional path to favicon for dark theme (resolved via static tag)
    - If no images provided, only text is shown

    Navigation configuration:
    - sidebar: Configuration dict or False to disable sidebar
        - collapsible: Boolean, whether sidebar can collapse to icon-only mode
        - show_at: Bootstrap 5 breakpoint ('sm', 'md', 'lg', 'xl', 'xxl')
                   Below this breakpoint, sidebar becomes an offcanvas element

    Returns:
        dict: Dictionary containing 'page_config' key with the configuration.
    """
    config = getattr(settings, "PAGE_CONFIG", {})
    # Set default layout to 'sidebar' if not specified
    if "layout" not in config:
        config = {**config, "layout": "sidebar"}
    return {
        "page_config": config,
    }
