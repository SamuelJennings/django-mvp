# Outer Layout Documentation

The outer layout system provides three layout modes controlled by `PAGE_CONFIG.layout_mode`.

## Layout Modes

### Navbar-Only

**Behaviour:**
- Sidebar is hidden by default
- Above breakpoint:
    - Navbar shows full navigation menu
- Below breakpoint:
    - Navbar shows hamburger toggle to open sidebar offcanvas
    - Site navigation in navbar is hidden
    - Site navigation accessible via sidebar offcanvas

**Configuration:**
```python
PAGE_CONFIG = {
    "layout_mode": "navbar",
    "navbar": {
        "breakpoint": "lg",  # Desktop navbar at lg+ (992px+)
    },
    ...
}
```

**Classes Applied:**
- `.mvp` gets `layout-navbar`
- `.mvp-navbar` gets `navbar-desktop-{breakpoint}` (or configured breakpoint)

**Utility Classes:**

Available within `navbar-desktop-{breakpoint}` media query:

- `.hide-on-mobile` - Hide element below navbar breakpoint
- `.hide-on-desktop` - Hide element at/above navbar breakpoint

---

### Sidebar Only

**Behaviour:**
- Sidebar is in-flow at/above specified breakpoint and hidden below
- Sidebar contains site navigation, actions, etc.
- Navbar is ONLY shown when sidebar is hidden
- Navbar only shows mobile style (hamburger toggle)

**Configuration:**
```python
PAGE_CONFIG = {
    "layout_mode": "sidebar",
    "sidebar": {
        "breakpoint": "lg",  # Sidebar in-flow at lg+ (992px+)
    }
}
```

**Classes Applied:**
- `.mvp` element gets `layout-sidebar hide-sidebar-lg`
- `.mvp-sidebar` gets `.sidebar-{breakpoint}` which places the sidebar in the document flow
<!-- - `.mvp-navbar`: Always mobile style (no desktop breakpoint) -->

**Utility Classes:**
- `.hide-if-sidebar-hidden` - Hide when sidebar is offcanvas (mobile)
- `.hide-if-sidebar-visible` - Hide when sidebar is in-flow (desktop)

---

### Navbar + Sidebar

**Configuration:**
```python
PAGE_CONFIG = {
    "layout_mode": "both",
}
```

**Classes Applied:**
- `.mvp` element: `layout-both`
- `.mvp-sidebar`: Always in-flow (never offcanvas), positioned relatively

**Behavior:**
- Sidebar always visible and in-flow at all screen sizes
- No responsive breakpoints
- No offcanvas behavior

**Utility Classes:**
- None - sidebar is always visible

---

## Element Structure

```
.mvp.layout-{mode}
├── .mvp-sidebar (offcanvas or in-flow based on mode)
└── .mvp-container
    ├── #page-navbar.navbar-desktop-{bp} (optional)
    └── .mvp-content
```

## Class Reference

| Class | Applied To | Purpose |
|-------|------------|---------|
| `.layout-navbar` | `.mvp` | Navbar-only layout mode |
| `.layout-sidebar` | `.mvp` | Responsive sidebar layout mode |
| `.layout-both` | `.mvp` | Both navbar and sidebar always visible |
| `.hide-sidebar-{bp}` | `.mvp` | Make sidebar offcanvas below breakpoint |
| `.navbar-desktop-{bp}` | `#page-navbar` | Desktop navbar at/above breakpoint |