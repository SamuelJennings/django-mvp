"""Custom menu renderers for django-mvp navigation."""

from __future__ import annotations

from typing import Any

from flex_menu.menu import MenuItem
from flex_menu.renderers import BaseRenderer


class AdminLTERenderer(BaseRenderer):
    """Renderer for AdminLTE 4 sidebar navigation.

    This renderer transforms django-flex-menus MenuItem objects into context data
    for AdminLTE-compatible templates. It provides:

    - MenuItem and MenuCollapse items maintain declaration order
    - MenuGroup items (section headers) sorted to bottom
    - Depth-based template selection for hierarchical menus
    - Active state detection based on current URL matching
    - Icon and badge rendering via extra_context
    - Bootstrap 5 compatible CSS classes and structure

    Templates are selected based on item depth and whether the item has children:
    - Depth 0: Container template (menus/container.html)
    - Depth 1+: Parent/leaf templates based on children presence

    Active state detection compares:
    1. Current request URL with menu item URL
    2. Current view name with menu item view_name
    3. Hierarchical active states for parent menu expansion
    """

    templates: dict[Any, Any] = {
        # Depth 0: Container (root menu)
        0: {"default": "menus/container.html"},
        # Depth 1+: Nested items (fallback)
        "default": {
            "parent": "menus/parent.html",
            "leaf": "menus/item.html",
        },
    }

    def get_context_data(self, item: MenuItem, **kwargs: Any) -> dict[str, Any]:
        """Build template context for rendering a menu item.

        Extracts label, URL, icon from extra_context and resolves view_name to URL.
        Sorts children at depth 0: MenuGroup items go to bottom, MenuItem/MenuCollapse maintain declaration order.
        """
        context = super().get_context_data(item, **kwargs)

        # Extract label from extra_context (fallback to item name)
        context["label"] = item.extra_context.get("label", item.name.replace("_", " ").title())

        # Extract icon if present
        context["icon"] = item.extra_context.get("icon")
        context["has_icon"] = bool(context["icon"])

        # URL is already resolved by django-flex-menus, but we'll pass it through
        # If URL resolution failed, use "#" as fallback
        if not context.get("url"):
            context["url"] = "#"

        # Extract additional CSS classes
        context["item_classes"] = item.extra_context.get("classes", "")
        context["link_classes"] = item.extra_context.get("link_classes", "")

        # Check if item has children
        context["has_children"] = bool(item.children)

        # Extract component_type for rendering decision
        # MenuGroup → "menu-group", MenuCollapse → "menu-collapse", MenuItem → None (uses menu-item)
        context["component_type"] = item.extra_context.get("component_type")

        # Sort children: MenuGroup to bottom, others in declaration order
        # Only sort at depth 0 (root menu container)
        children = context.get("children")
        if item.depth == 0 and children:
            menu_groups = []
            other_items = []

            for child in children:
                component_type = child.extra_context.get("component_type")
                if component_type == "menu.group":
                    menu_groups.append(child)
                else:
                    other_items.append(child)

            context["children"] = other_items + menu_groups

        # Extract badge information
        context["badge"] = item.extra_context.get("badge")
        context["badge_classes"] = item.extra_context.get("badge_classes", "text-bg-secondary")
        context["has_badge"] = bool(context["badge"])

        # Active state detection (T043)
        request = kwargs.get("request")
        context["is_active"] = self._is_active(item, request) if request else False

        # Menu open state for parents with active children (T045)
        context["is_open"] = self._has_active_descendant(item, request) if request else False
        context["has_active_child"] = context["is_open"]  # Alias for template compatibility

        return context

    def _is_active(self, item: MenuItem, request: Any) -> bool:
        """Detect if menu item is active based on current request.

        Compares the current request URL and view name with the menu item's
        URL and view_name to determine if this item represents the current page.

        Args:
            item: The menu item to check for active state
            request: Django HttpRequest object with current request context

        Returns:
            True if the menu item matches the current request, False otherwise

        Implementation details:
            1. Compares request.path with item.url (direct URL matching)
            2. Compares request.path with resolved URLs from extra_context
            3. Compares request.resolver_match.view_name with item.view_name
            4. Returns False if no request context is available
        """
        if not request:
            return False

        current_url = request.path

        # Try to match against item's URL (check multiple possible attributes)
        item_url = getattr(item, "url", None) or item.extra_context.get("url")
        if item_url and current_url == item_url:
            return True

        # Also check if URL was already resolved in context by parent class
        resolved_url = getattr(item, "_url", None)
        if resolved_url and current_url == resolved_url:
            return True

        # Try to match against resolved view_name
        if hasattr(request, "resolver_match") and request.resolver_match:
            current_view_name = request.resolver_match.view_name
            if hasattr(item, "view_name") and item.view_name == current_view_name:
                return True

        return False

    def _has_active_descendant(self, item: MenuItem, request: Any) -> bool:
        """Check if item has active descendants at any depth.

        Recursively traverses the menu hierarchy to determine if any child
        or nested child menu item is active. Used to apply 'menu-open' state
        to parent menu items when one of their descendants is active.

        Args:
            item: The parent menu item to check for active descendants
            request: Django HttpRequest object with current request context

        Returns:
            True if any descendant at any nesting level is active, False otherwise

        Implementation details:
            1. Returns False if no request context or no children
            2. Checks direct children with _is_active()
            3. Recursively checks nested children at all depths
            4. Short-circuits on first active descendant found (performance optimization)
        """
        if not request or not hasattr(item, "children"):
            return False

        # Check direct children
        for child in item.children:
            if self._is_active(child, request):
                return True
            # Recursively check nested children
            if self._has_active_descendant(child, request):
                return True

        return False


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
