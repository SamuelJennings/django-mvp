"""Custom menu renderers for FairDM navigation."""

from flex_menu.renderers import BaseRenderer


class NavbarRenderer(BaseRenderer):
    """Renderer for desktop navbar navigation.

    Maps menu item types to their corresponding navbar templates.
    Supports regular links, dropdowns with headers and items.
    """

    templates = {
        0: {"default": "menus/navbar/menu.html"},
        1: {
            "parent": "menus/navbar/nav_dropdown.html",
            "leaf": "menus/navbar/nav_link.html",
        },
        "default": {
            "parent": "menus/navbar/nav_dropdown.html",
            "leaf": "menus/navbar/dropdown_item.html",
        },
    }


class SidebarRenderer(BaseRenderer):
    """Renderer for sidebar/detail page menus.

    Used for plugin menus in detail views with categorized sections.
    """

    templates = {
        0: {"default": "menus/sidebar/menu.html"},
        1: {
            "parent": "menus/sidebar/section.html",
            "leaf": "menus/sidebar/item.html",
        },
        "default": {
            "parent": "menus/sidebar/section.html",
            "leaf": "menus/sidebar/item.html",
        },
    }


class DropdownRenderer(BaseRenderer):
    """Renderer for dropdown menus.

    Used for dropdown-style navigation elements.
    """

    templates = {
        0: {"default": "menus/dropdown/menu.html"},
        1: {
            "parent": "menus/dropdown/dropdown.html",
            "leaf": "menus/dropdown/item.html",
        },
        "default": {
            "parent": "menus/dropdown/dropdown.html",
            "leaf": "menus/dropdown/item.html",
        },
    }
