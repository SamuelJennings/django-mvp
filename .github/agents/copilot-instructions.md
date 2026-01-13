# django-cotton-layouts Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-23

## Active Technologies
- Python 3.10-3.12 + Django 4.2-5.x, django-cotton ≥2.3.1, django-cotton-bs5 ^0.5.1, Bootstrap 5.3, django-compressor ^4.5.1, django-libsass ^0.9 (002-inner-layout)
- N/A (component library) (002-inner-layout)
- Python 3.11+ / Django 4.2+ + django-cotton (Cotton component system with c-vars and slots), AdminLTE 4 (CSS framework) (001-layout-components)
- N/A (template-only refactor) (001-layout-components)
- Python 3.11+ + Django 4.2+, django-cotton (Cotton component system with c-vars and slots) (001-layout-components)
- N/A (template-only feature) (001-layout-components)
- Python 3.11+, Django 4.2+ + django-cotton (template engine), Bootstrap 5.3, AdminLTE 4, Bootstrap Icons (003-default-widgets)
- N/A (template-only components) (003-default-widgets)
- Python 3.10-3.12 + Django 4.2-5.x, django-cotton >=2.3.1, AdminLTE 4 (CSS via CDN) (002-layout-configuration)
- N/A (no database changes - template/static files only) (002-layout-configuration)
- Python 3.10-3.12 (Django MVP supports 3.10, 3.11, 3.12) + Django 4.2-5.x, django-flex-menus ^0.4.1, django-cotton ^2.3.1, django-easy-icons ^0.4.0, django-cotton-bs5 ^0.5.1 (004-site-navigation)
- N/A (menu configuration is code-based, not database-backed) (004-site-navigation)

- Python 3.11 (tests target) + Django, django-cotton, django-cotton-bs5, django-flex-menus, django-easy-icons, django-compressor, django-libsass, crispy-forms/bootstrap5 (001-outer-layout-config)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.11 (tests target): Follow standard conventions

## Recent Changes
- 004-site-navigation: Added Python 3.10-3.12 (Django MVP supports 3.10, 3.11, 3.12) + Django 4.2-5.x, django-flex-menus ^0.4.1, django-cotton ^2.3.1, django-easy-icons ^0.4.0, django-cotton-bs5 ^0.5.1
- 002-layout-configuration: Added Python 3.10-3.12 + Django 4.2-5.x, django-cotton >=2.3.1, AdminLTE 4 (CSS via CDN)
- 003-default-widgets: Added Python 3.11+, Django 4.2+ + django-cotton (template engine), Bootstrap 5.3, AdminLTE 4, Bootstrap Icons


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
