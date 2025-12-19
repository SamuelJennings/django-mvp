# Layout Configuration Guide

Django Cotton Layouts provides three flexible layout modes to suit different application needs. All layouts use responsive design principles and adapt seamlessly to mobile devices.

## Overview

The `layout` configuration controls **visibility at different screen sizes** for the sidebar and navbar components. Both components are always rendered in the DOM, with Bootstrap's responsive utilities controlling their visibility.

## Configuration Key

Add to your Django `settings.py`:

```python
PAGE_CONFIG = {
    "layout": "sidebar",  # Options: 'sidebar', 'navbar', or 'both'
    # ... other config
}
```

---

## Layout Modes

### 1. **Sidebar Layout** (Default)

**Best for**: Admin panels, documentation sites, desktop-first applications

**Desktop behavior**: Sidebar only  
**Mobile behavior**: Navbar with sidebar toggle

```python
PAGE_CONFIG = {
    "layout": "sidebar",
    "sidebar": {
        "collapsible": True,
        "width": "280px",
        "show_at": "lg",  # Sidebar visible on lg+ screens (≥992px)
    },
    "navbar": {
        "fixed": True,
        "border": True,
        "variant": "light",
    },
}
```

**Responsive Behavior**:
- **≥992px (lg and above)**: Sidebar visible, navbar hidden
- **<992px (below lg)**: Navbar visible, sidebar accessible via toggle (offcanvas)

**Use this when**: You want a traditional desktop application feel with a persistent sidebar

---

### 2. **Navbar Layout**

**Best for**: Marketing sites, blogs, public-facing web applications

**Desktop behavior**: Navbar only  
**Mobile behavior**: Navbar with sidebar toggle

```python
PAGE_CONFIG = {
    "layout": "navbar",
    "sidebar": {
        "width": "300px",
        "show_at": "lg",
    },
    "navbar": {
        "fixed": True,
        "border": True,
        "variant": "dark",
    },
}
```

**Responsive Behavior**:
- **All screen sizes**: Navbar always visible
- **Sidebar**: Completely hidden, only accessible via toggle button in navbar (opens as offcanvas)

**Use this when**: You want a modern, web-first design with top navigation

---

### 3. **Both Layout**

**Best for**: Complex dashboards, data-heavy applications, enterprise software

**Desktop behavior**: Both sidebar and navbar (navbar acts as utility bar)  
**Mobile behavior**: Navbar with sidebar toggle

```python
PAGE_CONFIG = {
    "layout": "both",
    "sidebar": {
        "collapsible": True,
        "width": "260px",
        "show_at": "xl",  # Both visible on xl+ screens (≥1200px)
    },
    "navbar": {
        "fixed": True,
        "border": True,
        "variant": "dark",
    },
}
```

**Responsive Behavior**:
- **≥1200px (xl and above)**: Both sidebar AND navbar visible simultaneously
- **<1200px (below xl)**: Navbar visible, sidebar accessible via toggle (offcanvas)

**Special Behavior**: When `layout='both'`, the navbar's brand, menu, and action widgets are **automatically hidden**. The navbar serves as a utility bar (search, profile, etc.) while the sidebar provides primary navigation.

**Use this when**: You need maximum navigation flexibility with both persistent sidebar and top navbar

---

## Complete Configuration Examples

### Minimal Sidebar Layout

```python
PAGE_CONFIG = {
    "layout": "sidebar",  # Optional: defaults to 'sidebar'
    "sidebar": {
        "show_at": "lg",
    },
}
```

### Production Navbar Layout

```python
PAGE_CONFIG = {
    "layout": "navbar",
    "brand": {
        "text": "My SaaS",
        "image_light": "img/logo-light.svg",
        "image_dark": "img/logo-dark.svg",
    },
    "sidebar": {
        "width": "300px",
        "show_at": "lg",
    },
    "navbar": {
        "fixed": True,
        "border": True,
        "variant": "dark",
        "start": {"navbar.brand": {}},
        "end": {"navbar.menu": {"menu": "navbar"}},
    },
    "actions": [
        {"icon": "github", "text": "GitHub", "href": "https://github.com/...", "target": "_blank"},
    ],
}
```

### Enterprise Both Layout

```python
PAGE_CONFIG = {
    "layout": "both",
    "brand": {
        "text": "Dashboard",
        "image_light": "img/logo-light.svg",
        "image_dark": "img/logo-dark.svg",
    },
    "sidebar": {
        "collapsible": True,
        "width": "280px",
        "show_at": "xl",  # Requires wider screens for both layouts
    },
    "navbar": {
        "fixed": True,
        "border": True,
        "variant": "dark",
        "start": {"navbar.brand": {}},
    },
    "actions": [
        {"icon": "add", "text": "New Project", "href": "/projects/new/"},
        {"icon": "settings", "text": "Settings", "href": "/settings/"},
    ],
}
```

---

## Breakpoint Reference

The `sidebar.show_at` setting uses Bootstrap 5 breakpoints:

| Breakpoint | Min Width | Typical Device |
|------------|-----------|----------------|
| `sm` | 576px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 992px | Desktop |
| `xl` | 1200px | Large desktop |
| `xxl` | 1400px | Extra large desktop |

**Recommendation**: 
- Use `lg` for `layout='sidebar'` (most common)
- Use `xl` for `layout='both'` (needs more space)

---

## Quick Comparison

| Layout | Desktop | Mobile | Navbar Content | Best For |
|--------|---------|--------|----------------|----------|
| `sidebar` | Sidebar only | Navbar + toggle | Brand, menu, actions | Admin panels, docs |
| `navbar` | Navbar only | Navbar + toggle | Brand, menu, actions | Marketing sites, blogs |
| `both` | Sidebar + navbar | Navbar + toggle | **Utilities only** (search, profile) | Dashboards, enterprise apps |

**Note**: When `layout='both'`, the navbar automatically hides brand, menu, and action widgets to avoid duplication with the sidebar.

---

## Migration Guide

If you're upgrading from a version without `layout` config:

**Before** (implicit behavior):
```python
PAGE_CONFIG = {
    "sidebar": {"show_at": "lg"},
    "navbar": {...},
}
```

**After** (explicit, same behavior):
```python
PAGE_CONFIG = {
    "layout": "sidebar",  # Makes it explicit
    "sidebar": {"show_at": "lg"},
    "navbar": {...},
}
```

The default is `"sidebar"`, so existing configurations continue to work without changes.

---

## Technical Details

### How It Works

1. **Both components are always rendered** in the HTML
2. **Responsive classes control visibility**:
   - `layout='sidebar'`: Navbar gets `d-lg-none` (hidden on large screens)
   - `layout='navbar'`: Sidebar gets `d-none` (always hidden)
   - `layout='both'`: Neither gets hidden classes
3. **Below breakpoint**: All layouts behave the same (navbar + offcanvas sidebar)

### CSS Classes Applied

**Sidebar (`layout='navbar'`)**:
```html
<div id="page-sidebar" class="offcanvas-lg d-none">
```

**Navbar (`layout='sidebar'`)**:
```html
<nav id="page-navbar" class="navbar d-lg-none">
```

**Both (`layout='both'`)**:
```html
<div id="page-sidebar" class="offcanvas-xl">
<nav id="page-navbar" class="navbar">
```

---

## Troubleshooting

**Q: My sidebar isn't showing on desktop**  
A: Check `layout` is set to `'sidebar'` or `'both'`, and `sidebar.show_at` matches your screen size

**Q: I want navbar on desktop too**  
A: Use `layout='both'`

**Q: Sidebar won't collapse to icons**  
A: Set `sidebar.collapsible: True` in your config

**Q: I need different breakpoints for sidebar and navbar**  
A: Currently, both use `sidebar.show_at`. For more granular control, consider adding a top-level `breakpoint` config (see roadmap)

---

## Roadmap

Future improvements being considered:

- [ ] Independent breakpoint control for sidebar and navbar
- [ ] `visibility` config for more granular control
- [ ] Additional layout modes (e.g., `navbar-top-sidebar-bottom`)

