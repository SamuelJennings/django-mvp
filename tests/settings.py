"""
Test-specific Django settings.

This module provides a stable, minimal configuration for testing.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = "test-secret-key-for-testing-only"

DEBUG = True

ALLOWED_HOSTS = ["*"]

USE_I18N = True

# Minimal app configuration for testing
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "compressor",
    "django_browser_reload",  # Optional, commented for testing
    "example",
    "mvp",
    "easy_icons",
    "crispy_forms",
    "crispy_bootstrap5",
    "flex_menu",
    "django_cotton",
    "cotton_bs5",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mvp.context_processors.mvp_config",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),  # Use persistent database file
    }
}

AUTH_PASSWORD_VALIDATORS = []

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "static")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

STATICFILES_DIRS = []

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)


# https://github.com/torchbox/django-libsass
LIBSASS_SOURCEMAPS = True


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}

CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Easy Icons configuration
EASY_ICONS = {
    "default": {
        "renderer": "easy_icons.renderers.ProviderRenderer",
        "config": {"tag": "i"},
        "icons": {
            # Navigation icons
            "arrow_right": "bi bi-arrow-right",
            "house": "bi bi-house",
            "sidebar": "bi bi-layout-sidebar",
            "navbar": "bi bi-window",
            "circle": "bi bi-circle",
            # Menu icons
            "grid": "bi bi-grid-3x3-gap",
            "box-seam": "bi bi-box-seam",
            "folder": "bi bi-folder",
            "newspaper": "bi bi-newspaper",
            "check2-square": "bi bi-check2-square",
            "layout-wtf": "bi bi-layout-wtf",
            "chevron_right": "bi bi-chevron-right",
            # Category icons
            "cpu": "bi bi-cpu",
            "shirt": "bi bi-shirt",
            "book": "bi bi-book",
            "home": "bi bi-house",
            "bicycle": "bi bi-bicycle",
            "laptop": "bi bi-laptop",
            "heart": "bi bi-heart",
            "briefcase": "bi bi-briefcase",
            # UI icons
            "calendar": "bi bi-calendar3",
            "calendar-event": "bi bi-calendar-event",
            "documentation": "bi bi-book",
            "filter": "bi bi-funnel",
            "github": "bi bi-github",
            "logout": "bi bi-box-arrow-right",
            "person": "bi bi-person",
            "person-circle": "bi bi-person-circle",
            "settings": "bi bi-gear",
            "theme_light": "bi bi-sun",
            "support": "bi bi-life-preserver",
            "eye": "bi bi-eye",
            "sort": "bi bi-sort-down",
            "search": "bi bi-search",
            # Status icons
            "check-circle-fill": "bi bi-check-circle-fill",
            "code-slash": "bi bi-code-slash",
            "info-circle": "bi bi-info-circle",
            # Default brand icon
            "database-fill": "bi bi-database-fill",
            # View mode icons
            "list-ul": "bi bi-list-ul",
            "table": "bi bi-table",
            # Action icons
            "add": "bi bi-plus-circle",
            "plus": "bi bi-plus-lg",
            "dash": "bi bi-dash-lg",
            "menu": "bi bi-list",
            # Example
            "cart": "bi bi-cart-fill",
            "graph-up": "bi bi-graph-up-arrow",
            "people": "bi bi-people",
            "link": "bi bi-link-45deg",
            "dollar": "bi bi-currency-dollar",
        },
    },
}

# Flex Menu configuration
FLEX_MENUS = {
    "renderers": {
        "adminlte": "mvp.renderers.AdminLTERenderer",
        "sidebar": "mvp.renderers.SidebarRenderer",
        "navbar": "mvp.renderers.NavbarRenderer",
        "dropdown": "mvp.renderers.DropdownRenderer",
    },
    "log_url_failures": DEBUG,
}

MVP = {
    "layout_mode": "sidebar",  # "navbar", "sidebar", or "both"
    "brand": {
        "text": "Django MVP",
        "image_light": "dac_bg_white.svg",  # Path to light theme logo
        "image_dark": "dac_bg_transparent.svg",  # Path to dark theme logo
        "icon_light": "icon.svg",  # Path to light theme icon/favicon
        "icon_dark": None,  # Path to dark theme icon/favicon (optional)
    },
    # Sidebar configuration (per-region keys only)
    "sidebar": {
        "breakpoint": "md",  # False = navbar-only mode (default per spec)
        # Or set to 'sm', 'md', 'lg', 'xl', 'xxl' to show in-flow at that breakpoint
        "collapsible": True,  # Whether sidebar can collapse to icon-only mode (default: True)
        # "width": "280px",  # Optional: custom sidebar width (default: 260px)
    },
    # Navbar configuration (per-region keys only)
    "navbar": {
        "fixed": False,  # Whether navbar is fixed to top (default: False)
        "border": False,  # Whether navbar has bottom border (default: False)
        "breakpoint": "md",  # Show navbar menu at this breakpoint (default: "sm" per spec)
        # Only applies when sidebar.breakpoint is False (navbar-only mode)
        # Set to False to never show navbar menu (sidebar toggle only)
        # Options: 'sm', 'md', 'lg', 'xl', 'xxl', or False
    },
    # Navigation actions (rendered in active region without duplication)
    "actions": [
        {
            "icon": "github",
            "text": "GitHub",
            "href": "https://github.com/django-mvp/django-mvp",
            "target": "_blank",
        },
        {
            "icon": "documentation",
            "text": "Documentation",
            "href": "/docs/",
            "target": "_blank",
        },
    ],
}
