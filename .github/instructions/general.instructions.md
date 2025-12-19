---
applyTo: '**'
---

# Copilot Instructions

These instructions apply to all code in this repository.  
Please follow them when suggesting code completions.

## IMPORTANT

Always use Context7 when you need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.

### Context7 Library Reference Guide

Use Context7 to fetch documentation for these libraries based on the task:

- `django/django` (topic: "templates") - Template syntax, tags, filters, template inheritance
- `wrabit/django-cotton` - Cotton template tags, components, layout system
- `samueljennings/django-easy-icons` - Icon usage, icon sets, customization
- `samueljennings/django-cotton-bs5` - Bootstrap 5 Cotton components, UI building blocks
- `samueljennings/django-flex-menus` - Menu definitions, rendering, dynamic menus
- `websites/getbootstrap_5_3` - Bootstrap 5.3 components, utilities, best practices

When working on a specific task, query the relevant library documentation first to ensure
you're using current APIs and best practices. Use mode='code' for implementation details
and mode='info' for conceptual understanding.

## Environment & Tooling
- **Poetry** is the package and environment manager.
- All Python-related commands must be prefixed with `poetry run ...`.
  - ✅ Example: `poetry run pytest`, `poetry run python manage.py migrate`
  - ❌ Do not use: `pytest`, `python manage.py ...`
- Dependencies are managed via `pyproject.toml` and `poetry.lock`.

### 🚨 CRITICAL: NEVER START THE DEVELOPMENT SERVER 🚨
- **The Django development server is ALREADY RUNNING** in a separate process.
- **DO NOT EXECUTE** `runserver` under ANY circumstances.
- **DO NOT RUN**: `poetry run python manage.py runserver`
- **DO NOT RUN**: `python manage.py runserver`
- **DO NOT START** the server even if you think it's not running.
- **DO NOT SUGGEST** starting the server to the user.
- If you cannot access localhost, INFORM THE USER but DO NOT attempt to start the server yourself.
- The server automatically reloads when code changes - you never need to restart it.

### Static Files Management
- **NEVER run `collectstatic`** command.
- Static files are compressed at runtime using django-compressor.
- CSS/JS changes are automatically detected and recompiled.
- ❌ Never use: `poetry run python manage.py collectstatic`

## Package overview
- This is a **Django app** providing application layouts and UI patterns.
- This app uses `django-cotton` for reusable template components.
- It ships reusable layout patterns and UI components as Django-Cotton templates (lives under templates/cotton/).
- It is designed to be used in Django projects requiring sophisticated navigation, list/detail views, and data-centric interfaces.
- All components should be aria compliant and accessible by default.
- Components build on top of `django-cotton-bs5` for base Bootstrap 5 components.

### Core Purpose
The primary goal of this package is to provide a **modern, sleek, and functional batteries-included starter pack** for creating data-driven dashboards and websites. It offers:

- **Zero-configuration layouts** that work out of the box
- **Centralized configuration** via Django settings
- **Minimal template customization** required from end users
- **Sophisticated UI patterns** for data-centric applications
- **Production-ready components** for research portals, admin interfaces, and institutional applications

### Configuration Architecture

#### The PAGE_CONFIG System
Django Cotton Layouts uses a **configuration-driven approach** where all layout behavior, branding, navigation, and UI settings are controlled via a single `PAGE_CONFIG` dictionary in Django settings.

**Context Processor:**
- `cotton_layouts.context_processors.page_config` injects `page_config` into all templates
- This makes configuration globally available without passing it explicitly in views
- Configuration is accessed as `{{ page_config.key }}` in templates

**Configuration Structure:**
```python
PAGE_CONFIG = {
    "layout": "sidebar",  # or "navbar"
    "brand": {
        "text": "Site Name",
        "image_light": "path/to/logo-light.svg",
        "image_dark": "path/to/logo-dark.svg",
        "icon_light": "path/to/favicon-light.svg",
        "icon_dark": "path/to/favicon-dark.svg",
    },
    "navigation": {
        "sidebar": {
            "collapsible": True,
            "show_at": "lg",  # Bootstrap breakpoint
            "width": "280px",  # Optional custom width
        },
    },
    "actions": [  # Action widgets in navigation
        {"icon": "github", "text": "GitHub", "href": "...", "target": "_blank"},
    ],
}
```

#### Template Hierarchy

The template system follows a strict hierarchy designed to minimize end-user customization:

1. **`base.html`** (package-level)
   - Foundation HTML structure
   - Loads Bootstrap, icons, and compiled SCSS
   - Configures favicons using `page_config.brand.icon_light/dark`
   - Includes JavaScript bundles
   - **NOT meant to be modified** by end users

2. **`layouts/base.html`** (package-level)
   - Minimal template that extends `base.html`
   - Provides extension points via blocks
   - Can be extended in user projects for global customizations (e.g., extra CSS/JS)

3. **`layouts/standard.html`** (package-level) ⭐ **KEY TEMPLATE**
   - Extends `layouts/base.html`
   - Implements the configured layout (sidebar or navbar)
   - Passes `page_config` to navigation components
   - Provides the `content` block for page-specific content
   - **This is where layout logic lives**

4. **Specialized layouts** (package-level)
   - `layouts/list_view.html` - Extends `standard.html`, adds list view patterns
   - `layouts/detail_view.html` - Extends `standard.html`, adds detail view patterns
   - `layouts/form_view.html` - Extends `standard.html`, adds form patterns

5. **User templates** (project-level)
   - Extend `layouts/standard.html` or specialized layouts
   - Override the `content` block
   - Focus only on page-specific content, not layout structure

#### Configuration Flow Through Components

Components receive configuration using Cotton's `:attrs` syntax:

**Example from `layouts/standard.html`:**
```html
<c-page.navigation.sidebar :attrs="page_config.navigation.sidebar"
                           :brand="page_config.brand" />
```

**How `:attrs` works:**
- `:attrs="dict"` expands a Python dictionary into component attributes
- If `page_config.navigation.sidebar = {"collapsible": True, "show_at": "lg"}`
- This becomes: `<c-page.navigation.sidebar collapsible="True" show_at="lg" />`

**Benefits:**
- Configuration is defined once in settings
- Components automatically receive their configuration
- No manual attribute passing required
- Easy to override or extend configuration

**Component-level consumption:**
```html
{# Inside a component like c-page.navigation.sidebar #}
<c-vars collapsible="False" show_at="md" width="260px" />

<div class="sidebar" 
     data-collapsible="{{ collapsible }}"
     data-show-at="{{ show_at }}"
     style="width: {{ width }}">
  ...
</div>
```

#### Key Design Patterns

1. **Extend, Don't Modify**
   - Users should extend `layouts/standard.html`, not modify package templates
   - Customizations happen in project-level templates
   - Package templates remain pristine and upgradable

2. **Block-based Customization**
   - Package templates provide strategic `{% block %}` tags
   - Users override blocks for targeted customizations
   - Example: `{% block extra_css %}` in `layouts/base.html`

3. **Configuration Over Code**
   - Behavior changes happen in `PAGE_CONFIG`, not template edits
   - Reduces need for template overrides
   - Centralizes all settings in one place

4. **Component Composition**
   - Layout templates compose smaller components
   - Components receive configuration via `:attrs`
   - Example: `<c-page.navigation.sidebar :attrs="page_config.navigation.sidebar" />`

#### Testing Components

When testing components that use configuration:
- Mock `page_config` in test context
- Test with various configuration dictionaries
- Verify `:attrs` expansion works correctly
- Test optional configuration keys (components should have sensible defaults)

Example:
```python
context = {
    "page_config": {
        "navigation": {
            "sidebar": {"collapsible": True, "show_at": "lg"}
        }
    }
}
html = render_to_string("layouts/standard.html", context)
```



## Linting & Style
- Follow **Ruff** linting rules (see `pyproject.toml`).
- For HTML/JS/CSS inside templates, follow **djlint** rules. (see `pyproject.toml`)

## Temporary Test Files
- The agent may create temporary Python files in the project root for experimentation.
- The name of such files must always follow the format: `tmp_*.py`.
- These files are **not part of the test suite** and must be deleted after use.
- Cleanup should happen automatically once the experiment is done.
- Temporary files should never be committed to version control.

## Testing
- Use **pytest** as the test framework (never unittest).
- Config is located in `pyproject.toml`, not `pytest.ini`.
- Test files are named `test_*.py`.
- Always run tests with:
  ```bash
  poetry run pytest
  ```
- All layout components should be tested individually with appropriate unit tests.
- Analyse a template component for default and named slots and ensure tests cover:
  - Rendering with default slot content.
  - Rendering with named slot content.
  - Rendering without optional slots.
- Test various arguments declared in `<c-vars>` with different values ensuring correct rendering.
- Test rendering using Django's render_to_string rather than full HTTP requests where possible for speed.
- Ensure no erroneous attributes appear as HTML attributes in the output. E.g. if a component takes {{ text }}, ensure `text="..."` does not appear in the rendered HTML by adding it to `<c-vars>`.
- When creating template strings for testing, there is no need to use `{% load cotton %}`.

## Layout Philosophy
- **Slot-based composition**: Use Cotton's slot system for flexible content areas
- **Responsive-first**: Mobile-friendly layouts that adapt to screen size
- **Integration-ready**: Works with flex-menus, easy-icons, and Bootstrap 5
- **Accessibility**: ARIA-compliant and keyboard-navigable
- **Progressive enhancement**: Start with semantic HTML, enhance with HTMX/Alpine.js
