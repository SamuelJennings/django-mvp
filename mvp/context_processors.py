"""Context processors for django-mvp."""

import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def mvp_config(request):
    """Provide MVP configuration to all templates.

    This context processor makes the MVP configuration dictionary available
    in all templates as 'mvp', allowing centralized control of layout,
    branding, and UI settings.

    The MVP configuration dictionary can contain:
    - brand: Site branding (text, logo, icon)
    - layout: AdminLTE layout options (fixed_sidebar, sidebar_expand, body_class)
    - sidebar: Sidebar configuration (visible, width)
    - footer: Footer configuration (visible, text)
    - actions: List of action widgets for navbar (icon, text, href, target)

    Example settings.py configuration:
        MVP = {
            'brand': {
                'text': 'My Application',
                'logo': 'img/logo.png',  # Optional logo image
                'icon': 'img/favicon.ico',  # Optional favicon
            },
            'layout': {
                'fixed_sidebar': True,
                'sidebar_expand': 'lg',  # When sidebar expands: sm, md, lg, xl, xxl
                'body_class': 'layout-fixed sidebar-expand-lg',
            },
            'sidebar': {
                'visible': True,
                'width': '280px',  # Optional custom width
            },
            'footer': {
                'visible': True,
                'text': '© 2026 My Application',
            },
            'actions': [
                {'icon': 'github', 'text': 'GitHub', 'href': 'https://github.com/...', 'target': '_blank'},
            ],
        }

    Returns:
        dict: Dictionary containing 'mvp' key with the configuration.
    """
    config = getattr(settings, "MVP", {})

    # Provide sensible defaults
    defaults = {
        "brand": {
            "text": "Django MVP",
            "logo": None,
            "icon": None,
        },
        "layout": {
            "fixed_sidebar": True,
            "sidebar_expand": "lg",
            "body_class": "layout-fixed sidebar-expand-lg bg-body-tertiary",
        },
        "sidebar": {
            "visible": True,
            "width": "280px",
        },
        "footer": {
            "visible": True,
            "text": None,
        },
        "actions": [],
    }

    # Merge user config with defaults
    merged_config = defaults.copy()
    for key, value in config.items():
        if isinstance(value, dict) and key in merged_config:
            merged_config[key] = {**merged_config[key], **value}
        else:
            merged_config[key] = value

    return {
        "mvp": merged_config,
    }
