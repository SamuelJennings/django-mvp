# Layout Configuration Guide

Django Cotton Layouts provides a flexible, configuration-driven outer layout system. Layout behavior is determined by **per-region settings** in the `PAGE_CONFIG` dictionary, allowing fine-grained control over navigation placement, branding, and responsive behavior.

## Overview

Django Cotton Layouts uses a **per-region configuration approach** where layout mode is derived from individual component settings rather than a top-level `layout` key. The primary control is `sidebar.show_at`:

- **`sidebar.show_at=False`** → Navbar-only mode (default)
- **`sidebar.show_at="lg"`** → Sidebar mode with primary navigation in sidebar
- **Actions and navigation render in the active region only** (no duplication)

## Configuration Key

Add to your Django `settings.py`:

```python
PAGE_CONFIG = {
    "brand": {...},
    "sidebar": {...},
    "navbar": {...},
    "actions": [...],
}
```

**JSON Schema**: See `specs/001-outer-layout-config/contracts/page_config.schema.json` for the complete contract.

---

## Layout Modes

### 1. **Navbar-Only Layout** (Default)

**Best for**: Marketing sites, blogs, public-facing web applications

**Desktop behavior**: Navbar with primary navigation  
**Mobile behavior**: Navbar with sidebar offcanvas

```python
PAGE_CONFIG = {
    "brand": {
        "text": "My Site",
        "image_light": "img/logo-light.svg",
        "image_dark": "img/logo-dark.svg",
    },
    "sidebar": {
        "show_at": False,  # Navbar-only mode
        "collapsible": True,  # Sidebar available via offcanvas
        "width": "280px",
    },
    "navbar": {
        "fixed": False,
        "border": False,
        "menu_visible_at": "sm",  # Show primary menu from sm breakpoint
    },
    "actions": [
        {"icon": "github", "text": "GitHub", "href": "https://github.com/..."},
    ],
}
```

**Responsive Behavior**:
- **All screen sizes**: Navbar visible with brand and actions
- **≥576px (sm and above)**: Primary navigation menu visible in navbar
- **<576px (below sm)**: Primary navigation accessible via sidebar offcanvas toggle
- **Actions**: Rendered in navbar (active region)

**Use this when**: You want a modern, web-first design with top navigation

---

### 2. **Sidebar Layout**

**Best for**: Admin panels, documentation sites, desktop-first applications

**Desktop behavior**: Sidebar with primary navigation, navbar for utilities  
**Mobile behavior**: Navbar with sidebar offcanvas toggle

```python
PAGE_CONFIG = {
    "brand": {
        "text": "Admin Dashboard",
        "image_light": "img/logo-light.svg",
        "image_dark": "img/logo-dark.svg",
    },
    "sidebar": {
        "show_at": "lg",  # Sidebar visible on lg+ screens (≥992px)
        "collapsible": True,
        "width": "260px",
    },
    "navbar": {
        "fixed": True,
        "border": True,
        "menu_visible_at": False,  # Ignored when sidebar in-flow
    },
    "actions": [
        {"icon": "add", "text": "New", "href": "/new/"},
        {"icon": "settings", "text": "Settings", "href": "/settings/"},
    ],
}
```

**Responsive Behavior**:
- **≥992px (lg and above)**: Sidebar visible with brand, primary navigation, and actions
- **<992px (below lg)**: Navbar visible, sidebar accessible via toggle (offcanvas)
- **Actions**: Rendered in sidebar when in-flow, navbar when offcanvas
- **Primary navigation**: Always in sidebar (never duplicated in navbar)

**Use this when**: You want a traditional desktop application feel with persistent sidebar

**Important**: When `sidebar.show_at` is a breakpoint, `navbar.menu_visible_at` is automatically ignored to prevent duplicate navigation rendering

---

## Configuration Schema

### Top-Level Keys

```python
PAGE_CONFIG = {
    "brand": {...},      # Required: Brand identity configuration
    "sidebar": {...},    # Required: Sidebar component configuration
    "navbar": {...},     # Required: Navbar component configuration  
    "actions": [...],    # Required: Global action widgets (can be empty list)
}
```

### Brand Configuration

```python
"brand": {
    "text": "Site Name",              # Required: Fallback text
    "image_light": "path/logo.svg",   # Optional: Light theme brand image
    "image_dark": "path/logo.svg",    # Optional: Dark theme brand image
    "icon_light": "path/icon.svg",    # Optional: Light theme favicon
    "icon_dark": "path/icon.svg",     # Optional: Dark theme favicon
}
```

**Fallback Behavior**: If theme-appropriate image is missing, brand text is displayed with full accessibility preserved.

### Sidebar Configuration

```python
"sidebar": {
    "show_at": False,     # False/None (navbar-only) or "sm"|"md"|"lg"|"xl"|"xxl" (sidebar mode)
    "collapsible": True,  # Optional: Allow sidebar collapse (default: True)
    "width": "280px",     # Optional: Sidebar width (default: "260px")
}
```

**Key Behaviors**:
- `show_at=False` → Navbar-only mode (sidebar offcanvas only)
- `show_at="lg"` → Sidebar in-flow at ≥992px, offcanvas below
- When sidebar is in-flow, `navbar.menu_visible_at` is ignored (prevents duplication)

### Navbar Configuration

```python
"navbar": {
    "fixed": False,            # Optional: Fixed positioning (default: False)
    "border": False,           # Optional: Bottom border (default: False)
    "menu_visible_at": "sm",   # Optional: Breakpoint for primary menu (default: "sm")
                              # Ignored when sidebar.show_at is a breakpoint
}
```

**Key Behaviors**:
- `menu_visible_at` only applies in navbar-only mode (`sidebar.show_at=False`)
- When sidebar is in-flow, navbar never shows primary navigation

### Actions Configuration

```python
"actions": [
    {
        "icon": "github",                    # Required: Icon name (django-easy-icons)
        "text": "GitHub",                    # Required: Accessible text label
        "href": "https://github.com/...",   # Required: Link target
        "target": "_blank",                  # Optional: Link target attribute
        "id": "github-action",               # Optional: HTML id attribute
    },
]
```

**Rendering Rules**:
- Actions render in the **active navigation region only** (no duplication)
- When `sidebar.show_at` is a breakpoint → actions in sidebar
- When `sidebar.show_at=False` → actions in navbar
- Below sidebar breakpoint → actions move to navbar with sidebar

---

## Complete Configuration Examples

### Minimal Navbar-Only (Default)

```python
# Uses all defaults - no config needed, but can customize:
PAGE_CONFIG = {
    "brand": {"text": "My Site"},
    "sidebar": {"show_at": False},
    "navbar": {"menu_visible_at": "sm"},
    "actions": [],
}
```

### Production Navbar Layout

```python
PAGE_CONFIG = {
    "brand": {
        "text": "My SaaS",
        "image_light": "img/logo-light.svg",
        "image_dark": "img/logo-dark.svg",
        "icon_light": "img/favicon-light.svg",
        "icon_dark": "img/favicon-dark.svg",
    },
    "sidebar": {
        "show_at": False,  # Navbar-only
        "collapsible": True,
        "width": "300px",
    },
    "navbar": {
        "fixed": True,
        "border": True,
        "menu_visible_at": "sm",  # Primary menu visible from sm up
    },
    "actions": [
        {"icon": "github", "text": "GitHub", "href": "https://github.com/...", "target": "_blank"},
        {"icon": "user", "text": "Profile", "href": "/profile/"},
    ],
}
```

### Desktop Sidebar Layout

```python
PAGE_CONFIG = {
    "brand": {
        "text": "Dashboard",
        "image_light": "img/logo-light.svg",
        "image_dark": "img/logo-dark.svg",
    },
    "sidebar": {
        "show_at": "lg",  # Sidebar mode - in-flow at ≥992px
        "collapsible": True,
        "width": "280px",
    },
    "navbar": {
        "fixed": True,
        "border": True,
        "menu_visible_at": False,  # Ignored - sidebar controls navigation
    },
    "actions": [
        {"icon": "add", "text": "New Project", "href": "/projects/new/"},
        {"icon": "settings", "text": "Settings", "href": "/settings/"},
    ],
}
```

---

## Breakpoint Reference

The `sidebar.show_at` and `navbar.menu_visible_at` settings use Bootstrap 5 breakpoints:

| Breakpoint | Min Width | Typical Device |
|------------|-----------|----------------|
| `sm` | 576px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 992px | Desktop |
| `xl` | 1200px | Large desktop |
| `xxl` | 1400px | Extra large desktop |

**Validation**: Invalid breakpoint values trigger a warning and fallback to safe defaults (logged via Django's logging system).

**Recommendations**: 
- Use `"sm"` for `navbar.menu_visible_at` in navbar-only mode (most mobile-friendly)
- Use `"lg"` for `sidebar.show_at` in sidebar mode (most common desktop breakpoint)
- Use `"xl"` for `sidebar.show_at` when you need more horizontal space

---

## Quick Comparison

| Configuration | Desktop | Mobile | Navigation Location | Actions Location | Best For |
|---------------|---------|--------|---------------------|------------------|----------|
| `sidebar.show_at=False` | Navbar | Navbar + offcanvas | Navbar from `menu_visible_at` | Navbar | Marketing, blogs |
| `sidebar.show_at="lg"` | Sidebar | Navbar + offcanvas | Always sidebar | Sidebar (desktop), Navbar (mobile) | Admin panels, docs |

**Key Rule**: Navigation and actions **never duplicate**. They render in the active region based on `sidebar.show_at` and viewport size.

---

## Default Configuration

Out of the box, Django Cotton Layouts uses these defaults (requires no configuration):

```python
# Implicit defaults - no PAGE_CONFIG needed
{
    "brand": {
        "text": "Django MVP",
    },
    "sidebar": {
        "show_at": False,      # Navbar-only mode
        "collapsible": True,
        "width": "260px",
    },
    "navbar": {
        "fixed": False,
        "border": False,
        "menu_visible_at": "sm",  # Primary menu from sm up
    },
    "actions": [],
}
```

**Override any key** to customize behavior. Missing optional keys fall back to these defaults.

---

## Context Processor Integration

Configuration is exposed to templates via `mvp.context_processors.page_config`:

```python
# settings.py
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ...
                'mvp.context_processors.page_config',
            ],
        },
    },
]
```

Templates access configuration via `{{ page_config }}`:

```html
{# layouts/standard.html - passing config to components #}
<c-structure.sidebar :attrs="page_config.sidebar" :brand="page_config.brand" />
<c-structure.navbar :attrs="page_config.navbar" :brand="page_config.brand" />
```

**Dynamic Attrs (`:attrs`)**: Cotton's `:attrs` syntax expands dictionaries into component attributes, enabling configuration passthrough without manual attribute mapping.

---

## Migration Guide

If you're upgrading from a version with the old `layout` key:

**Before** (old system with top-level layout key):
```python
PAGE_CONFIG = {
    "layout": "navbar",  # Top-level layout key
    "sidebar": {"show_at": "lg"},
    "navbar": {...},
}
```

**After** (new per-region system):
```python
PAGE_CONFIG = {
    # No top-level layout key
    "sidebar": {"show_at": False},  # False = navbar-only
    "navbar": {"menu_visible_at": "sm"},
    # ... rest of config
}
```

**Migration Steps**:
1. Remove `"layout"` key
2. Set `sidebar.show_at`:
   - `layout="navbar"` → `sidebar.show_at=False`
   - `layout="sidebar"` → `sidebar.show_at="lg"` (or your preferred breakpoint)
   - `layout="both"` → Not directly supported; sidebar mode provides similar behavior
3. Add `navbar.menu_visible_at="sm"` for navbar-only mode
4. Ensure `actions` is a list (not nested under navigation)

---

## Technical Details

### How It Works

1. **Context processor** validates and enriches `PAGE_CONFIG` from settings
2. **Defaults applied** for missing keys during context processing
3. **Templates consume config** via Cotton's `:attrs` dynamic attribute syntax
4. **Components render conditionally** based on `sidebar.show_at` and viewport
5. **Responsive classes applied** automatically based on breakpoint configuration

### Single-Source Navigation Principle

Django Cotton Layouts enforces **zero duplicate navigation** rendering:

- **When `sidebar.show_at` is a breakpoint** (e.g., `"lg"`):
  - Primary navigation: Sidebar only (at all viewports)
  - Actions: Sidebar when in-flow (≥breakpoint), navbar when offcanvas (<breakpoint)
  - `navbar.menu_visible_at`: Ignored (logged warning if set)

- **When `sidebar.show_at=False`** (navbar-only mode):
  - Primary navigation: Navbar from `menu_visible_at` breakpoint up
  - Actions: Always navbar
  - Below `menu_visible_at`: Navigation available via sidebar offcanvas

### CSS Classes Applied

**Sidebar (navbar-only mode, `show_at=False`)**:
```html
<!-- Always offcanvas, never in-flow -->
<div id="page-sidebar" class="offcanvas offcanvas-start">
```

**Sidebar (sidebar mode, `show_at="lg"`)**:
```html
<!-- In-flow at ≥lg, offcanvas below -->
<div id="page-sidebar" class="offcanvas-lg offcanvas-start">
```

**Navbar (responsive visibility based on sidebar)**:
```html
<!-- Example: Hidden when sidebar in-flow at ≥lg -->
<nav id="page-navbar" class="navbar d-lg-none">
```

---

## Troubleshooting

**Q: My sidebar isn't showing on desktop**  
A: Check `sidebar.show_at` is set to a breakpoint like `"lg"` (not `False`), and verify your viewport width meets the breakpoint minimum.

**Q: I see duplicate navigation in both sidebar and navbar**  
A: This should never happen. Check your `sidebar.show_at` setting:
- If it's a breakpoint → navbar should never show primary navigation
- If it's `False` → navigation should only appear in navbar
- Review console/logs for configuration warnings

**Q: Actions aren't showing in the navbar**  
A: Check if `sidebar.show_at` is a breakpoint and your viewport is above that breakpoint. Actions move to the sidebar when it's in-flow.

**Q: Sidebar won't collapse to icons**  
A: Set `sidebar.collapsible=True` in your config. Ensure the sidebar component templates support collapse behavior.

**Q: Invalid breakpoint warning in logs**  
A: Use only valid Bootstrap 5 breakpoints: `"sm"`, `"md"`, `"lg"`, `"xl"`, `"xxl"`. Typos like `"large"` or `"desktop"` will trigger fallback to defaults.

**Q: Brand images not showing**  
A: Verify paths are correct and files exist. Check `STATIC_URL` is configured properly. If images are missing, the system falls back to `brand.text` display.

**Q: How do I get both sidebar and navbar with navigation?**  
A: This is intentionally not supported to prevent duplicate navigation. Use sidebar mode (`sidebar.show_at="lg"`) - the navbar remains present for utilities, search, profile, etc., but primary navigation stays in the sidebar.

---

## Best Practices

### 1. Start with Defaults
The default configuration (navbar-only, `sidebar.show_at=False`) works for most projects. Only customize when you have specific needs.

### 2. Choose the Right Breakpoint
- **Mobile-first sites**: Use `sidebar.show_at=False` (navbar-only)
- **Desktop-first apps**: Use `sidebar.show_at="lg"` 
- **Wide dashboards**: Use `sidebar.show_at="xl"` if you have complex layouts

### 3. Test Responsive Behavior
Always test your layout at:
- Mobile (<576px)
- Tablet (768px)
- Desktop (992px or 1200px depending on breakpoint)

### 4. Use Brand Images Wisely
Provide both light and dark theme images for professional appearance. Keep file sizes small (<20KB) for fast loading.

### 5. Keep Actions Minimal
Limit actions to 2-4 items. Too many actions clutter the navigation. Consider user menu dropdowns for profile/settings.

### 6. Leverage Dynamic Attrs
When building custom components that consume `page_config`, use `:attrs` for clean configuration passthrough:

```html
<c-my-component :attrs="page_config.sidebar" />
```

This automatically passes all sidebar config keys as component attributes.

---

## Roadmap

Future improvements being considered:

- [ ] Independent breakpoint control for sidebar visibility vs primary navigation placement
- [ ] Additional responsive control patterns (e.g., sidebar auto-collapse on scroll)
- [ ] Enhanced navbar utility area configuration for search, notifications, user menu
- [ ] Theme variant support beyond light/dark (custom color schemes)
- [ ] Per-page configuration overrides via view context

See project issues and milestones for discussion and status.