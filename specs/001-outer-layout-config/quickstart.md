# Quickstart: Outer Layout Configuration

## 1) Install and configure apps

Add to INSTALLED_APPS (see tests/settings.py for reference):
- mvp, django_cotton, django-cotton-bs5, flex_menu, easy_icons, compressor, crispy_forms, crispy_bootstrap5

## 2) Enable context processor

Add to Django TEMPLATES context_processors:
- mvp.context_processors.page_config

## 3) Define PAGE_CONFIG

Example (per-region config only):

```python
PAGE_CONFIG = {
    "brand": {"text": "Django MVP", "image_light": "dac_bg_white.svg", "image_dark": "dac_bg_transparent.svg", "icon_light": "icon.svg", "icon_dark": None},
    "sidebar": {"show_at": False, "collapsible": True},
    "navbar": {"fixed": False, "menu_visible_at": "lg"},
    "actions": [{"icon": "github", "text": "GitHub", "href": "https://github.com/django-mvp/django-mvp", "target": "_blank"}],
}
```

## 4) Use the standard layout

In your app templates:

```django
{% extends "layouts/standard.html" %}
{% block content %}
  <h1>Hello</h1>
{% endblock %}
```

The layout template consumes `page_config` via Cotton dynamic attrs:
- Sidebar: `:attrs="page_config.sidebar"`, `:brand="page_config.brand"`
- Navbar: `:attrs="page_config.navbar"`, `:brand="page_config.brand"`

## 5) Verify constitution gates (spot check)
- No duplicate primary navigation between navbar and sidebar
- Renders without any CSS framework present
- Inner layout remains template-only
- Accessible landmarks and focus order
- Theming via Sass/CSS variables (optional)
- JS optional; compiled assets only if behaviors are enabled
