from django.apps import apps


def app_is_installed(app_name: str) -> bool:
    """
    Check if a Django app is installed.

    Args:
        app_name: The app name or app config label to check for.
                  Can be either the full path (e.g., "crispy_forms")
                  or a label (e.g., "admin").

    Returns:
        bool: True if the app is installed in INSTALLED_APPS, False otherwise.

    Example:
        >>> from mvp.utils import app_is_installed
        >>> CRISPY_FORMS = app_is_installed("crispy_forms")
        >>> if CRISPY_FORMS:
        ...     from crispy_forms.helper import FormHelper
    """
    return apps.is_installed(app_name)


BS5_ICONS = {
    "arrow_right": "bi bi-arrow-right",
    "home": "bi bi-house",
    "sidebar-right": "bi bi-layout-sidebar-reverse",
    "sidebar-left": "bi bi-layout-sidebar",
    "navbar": "bi bi-window",
    "circle": "bi bi-circle",
    "filter": "bi bi-funnel",
    "github": "bi bi-github",
    "logout": "bi bi-box-arrow-right",
    "person": "bi bi-person",
    "people": "bi bi-people",
    "settings": "bi bi-gear",
    "theme_light": "bi bi-sun",
    "theme_dark": "bi bi-moon-stars-fill",
    "theme_auto": "bi bi-circle-half",
    "sort": "bi bi-sort-down",
    "search": "bi bi-search",
    "table": "bi bi-table",
    "menu": "bi bi-list",
    "dash": "bi bi-dash-lg",
    "maximize": "bi bi-arrows-fullscreen",
    "minimize": "bi bi-arrows-angle-contract",
}
