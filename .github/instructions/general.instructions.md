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
- This is a **Django app** providing AdminLTE 4 layouts and components.
- This app uses `django-cotton` for reusable template components.
- It ships AdminLTE-specific components as Django-Cotton templates (lives under templates/cotton/adminlte/).
- It is designed to be used in Django projects requiring sophisticated admin dashboards and data-centric interfaces.
- All components should be aria compliant and accessible by default.
- Standard Bootstrap 5 components are provided by `django-cotton-bs5` package.

### 🚨 CRITICAL: Cotton Component Naming Convention 🚨
- **Cotton components ALWAYS use snake_case (kebab-case)**, never camelCase or PascalCase
- ✅ Correct: `<c-adminlte.small-box />` or `<c-adminlte.info_box />`
- ❌ Wrong: `<c-adminlte.smallBox />` or `<c-adminlte.SmallBox />`
- Component file names: `small-box.html`, `info-box.html`, `timeline-item.html`
- Component usage: `<c-adminlte.small-box />`, `<c-adminlte.info-box />`, `<c-adminlte.timeline-item />`
- This is a **fundamental requirement** of django-cotton and must be followed strictly

### Architecture

Django MVP mirrors AdminLTE 4's grid-based layout structure:

```
.app-wrapper (grid container)
├── .app-sidebar (navigation)
├── .app-header (top navbar)
├── .app-main (content area)
│   ├── .app-content-header (page header/breadcrumbs)
│   └── .app-content (main content)
└── .app-footer (optional footer)
```

All layout behavior is controlled via the `MVP` configuration object in Django settings, requiring minimal template customization.

### Core Purpose
The primary goal of this package is to provide AdminLTE 4 for Django as reusable Cotton components:

- **AdminLTE 4 Layout System** - Full grid-based app-wrapper structure
- **Configuration-Driven Design** - Control via Django settings
- **AdminLTE-Specific Components** - Cards, boxes, widgets, timeline, chat, etc.
- **Bootstrap 5 Foundation** - Works with django-cotton-bs5 for base components
- **Production-Ready** - Designed for data-centric applications and admin interfaces

### Configuration Architecture

#### The MVP Configuration System
Django MVP uses a **configuration-driven approach** where all layout behavior, branding, and UI settings are controlled via the `MVP` dictionary in Django settings.

**Context Processor:**
- `mvp.context_processors.mvp_config` injects `mvp` into all templates
- This makes configuration globally available without passing it explicitly in views
- Configuration is accessed as `{{ mvp.key }}` in templates

**Configuration Structure:**
```python
MVP = {
    "brand": {
        "text": "My Application",
        "logo": "img/logo.png",  # Optional logo image
        "icon": "img/favicon.ico",  # Optional favicon
    },
    "layout": {
        "fixed_sidebar": True,
        "sidebar_expand": "lg",  # When sidebar expands: sm, md, lg, xl, xxl
        "body_class": "layout-fixed sidebar-expand-lg",
    },
    "sidebar": {
        "visible": True,
        "width": "280px",  # Optional custom width
    },
    "footer": {
        "visible": True,
        "text": "© 2026 My Application",
    },
    "actions": [  # Action buttons/links in navbar
        {"icon": "github", "text": "GitHub", "href": "...", "target": "_blank"},
    ],
}
```

#### Template Hierarchy

The template system follows a simple hierarchy:

1. **`base.html`** - Foundation HTML structure with AdminLTE CSS/JS from CDN
2. **`layouts/adminlte.html`** - AdminLTE app-wrapper layout structure with blocks
3. **User templates** - Extend `layouts/adminlte.html` and override blocks

**Key blocks in layouts/adminlte.html:**
- `page_title` - Page title in header
- `breadcrumbs` - Breadcrumb navigation
- `sidebar_menu` - Sidebar menu items
- `navbar_left` - Left navbar items
- `navbar_right` - Right navbar items
- `content` - Main page content
- `app_header`, `app_sidebar`, `app_footer` - Full layout sections

#### Key Design Patterns

1. **Extend, Don't Modify**
   - Users extend `layouts/adminlte.html`, not modify package templates
   - Customizations happen in project-level templates
   - Package templates remain pristine and upgradable

2. **Block-based Customization**
   - Layout template provides strategic `{% block %}` tags
   - Users override blocks for targeted customizations
   - Example: `{% block extra_css %}` in `base.html`

3. **Configuration Over Code**
   - Behavior changes happen in `MVP`, not template edits
   - Reduces need for template overrides
   - Centralizes all settings in one place

4. **Component Composition**
   - Use AdminLTE components via Cotton: `<c-adminlte.small-box />`
   - Use Bootstrap 5 components via django-cotton-bs5: `<c-bs5.button />`

## Linting & Style
- Follow **Ruff** linting rules (see `pyproject.toml`).
- For HTML/JS/CSS inside templates, follow **djlint** rules. (see `pyproject.toml`)

## Temporary Test Files
- The agent may create temporary Python files in the project root for experimentation.
- The name of such files must always follow the format: `tmp_*.py`.
- These files are **not part of the test suite** and must be deleted after use.
- Cleanup should happen automatically once the experiment is done.
- Temporary files should never be committed to version control.

## Layout Philosophy
- **Slot-based composition**: Use Cotton's slot system for flexible content areas
- **Responsive-first**: Mobile-friendly layouts that adapt to screen size
- **Integration-ready**: Works with flex-menus, easy-icons, and Bootstrap 5
- **Accessibility**: ARIA-compliant and keyboard-navigable
- **Progressive enhancement**: Start with semantic HTML, enhance with HTMX/Alpine.js
