# AdminLTE 4 Layout Behavior Analysis

This document provides a comprehensive analysis of AdminLTE 4's layout options based on inspection of the official demo site (https://adminlte.io/themes/v4/). Each layout was tested in a browser to understand its actual behavior.

## Overview

AdminLTE 4 provides 10 distinct layout variations that control how the main structural components (sidebar, header, footer) behave during scrolling and responsive interactions. The layouts are built on a CSS Grid-based `.app-wrapper` structure.

---

## 1. Default Sidebar (Unfixed Layout)

**URL:** `layout/unfixed-sidebar.html`

### Body Classes
```
sidebar-expand-lg sidebar-open bg-body-tertiary app-loaded hold-transition
```

### Behavior
- **Sidebar Position:** `static` - Scrolls with page content
- **Header Position:** `relative` - Scrolls with page content
- **Footer Position:** `static` - Scrolls with page content
- **Description:** This is the most basic layout where all components scroll naturally with the page. When you scroll down, the sidebar, header, and footer all move out of view.

### Use Case
- Simple applications with minimal navigation complexity
- When you want traditional scrolling behavior
- Content-heavy pages where sticky elements might obstruct content

---

## 2. Fixed Sidebar

**URL:** `layout/fixed-sidebar.html`

### Body Classes
```
layout-fixed sidebar-expand-lg sidebar-open bg-body-tertiary app-loaded hold-transition
```

### Behavior
- **Sidebar Position:** `sticky` - Remains fixed in viewport
- **Header Position:** `relative` - Scrolls with page content
- **Footer Position:** `static` - Scrolls with page content
- **Key Class:** `.layout-fixed`

### Use Case
- Applications where navigation menu needs to remain accessible
- Long pages with frequent need to access sidebar menu items
- Dashboard applications with navigation-heavy workflows

---

## 3. Fixed Header

**URL:** `layout/fixed-header.html`

### Body Classes
```
fixed-header sidebar-expand-lg sidebar-open bg-body-tertiary app-loaded hold-transition
```

### Behavior
- **Sidebar Position:** `static` - Scrolls with page content
- **Header Position:** `sticky` - Remains fixed at top of viewport
- **Footer Position:** `static` - Scrolls with page content
- **Key Class:** `.fixed-header`

### Use Case
- Applications where branding and top navigation must remain visible
- When user profile/notifications in header need constant access
- Search-heavy interfaces where header search needs to be always available

---

## 4. Fixed Footer

**URL:** `layout/fixed-footer.html`

### Body Classes
```
fixed-footer sidebar-expand-lg sidebar-open bg-body-tertiary app-loaded hold-transition
```

### Behavior
- **Sidebar Position:** `static` - Scrolls with page content
- **Header Position:** `relative` - Scrolls with page content
- **Footer Position:** `sticky` - Remains fixed at bottom of viewport
- **Key Class:** `.fixed-footer`

### Use Case
- Applications with important footer actions or information
- Forms or wizards where submit buttons are in the footer
- Copyright or legal information that must remain visible

---

## 5. Fixed Complete

**URL:** `layout/fixed-complete.html`

### Body Classes
```
layout-fixed fixed-header fixed-footer sidebar-expand-lg sidebar-open bg-body-tertiary app-loaded hold-transition
```

### Behavior
- **Sidebar Position:** `sticky` - Remains fixed in viewport
- **Header Position:** `sticky` - Remains fixed at top of viewport
- **Footer Position:** `sticky` - Remains fixed at bottom of viewport
- **Key Classes:** `.layout-fixed`, `.fixed-header`, `.fixed-footer`

### Visual Effect
All three major layout components remain fixed, creating an "application frame" where only the main content area scrolls.

### Use Case
- Full application dashboards
- Admin panels where all navigation must be persistently accessible
- Data-intensive applications requiring constant access to controls
- Applications mimicking native desktop software behavior

---

## 6. Layout + Custom Area

**URL:** `layout/layout-custom-area.html`

### Body Classes
```
layout-fixed sidebar-expand-lg sidebar-open bg-body-tertiary app-loaded hold-transition
```

### Behavior
- **Sidebar Position:** `sticky` - Remains fixed in viewport
- **Header Position:** `relative` - Scrolls with page content
- **Footer Position:** `static` - Scrolls with page content
- **Special Feature:** Custom content areas above and below main content

### Visual Structure
```
┌─────────────────────┐
│   Header            │
├─────────────────────┤
│ App Content Top     │ ← Custom Area (e.g., "Create Admin" button)
├─────────────────────┤
│   Main Content      │
├─────────────────────┤
│ App Content Bottom  │ ← Custom Area (e.g., "Refresh" button)
├─────────────────────┤
│   Footer            │
└─────────────────────┘
```

### Use Case
- Applications needing contextual action bars
- Dashboards with global actions that should appear before/after content
- Forms with toolbar buttons that need to scroll with content
- Applications with notification bars or announcement areas

---

## 7. Sidebar Mini

**URL:** `layout/sidebar-mini.html`

### Body Classes
```
layout-fixed sidebar-expand-lg sidebar-mini bg-body-tertiary app-loaded hold-transition sidebar-collapse
```

### Behavior
- **Sidebar Position:** `sticky` - Remains fixed in viewport
- **Sidebar Width:** `73.5938px` - Collapsed to show only icons
- **Key Classes:** `.layout-fixed`, `.sidebar-mini`, `.sidebar-collapse`

### Visual Effect
The sidebar collapses to show only icons, maximizing content area. On hover, menu items can expand to show full text.

### Use Case
- Applications where screen real estate is premium
- Dashboards with wide data tables or charts
- Users familiar with the interface who recognize icons
- Mobile-responsive designs where sidebar needs to be compact

---

## 8. Sidebar Mini + Collapsed

**URL:** `layout/collapsed-sidebar.html`

### Body Classes
```
layout-fixed sidebar-expand-lg sidebar-mini sidebar-collapse bg-body-tertiary app-loaded hold-transition
```

### Behavior
- **Sidebar Position:** `sticky` - Remains fixed in viewport
- **Sidebar Width:** `73.5938px` - Collapsed to show only icons
- **Key Classes:** `.layout-fixed`, `.sidebar-mini`, `.sidebar-collapse`

### Difference from Sidebar Mini
This layout appears visually identical to Sidebar Mini (#7). The difference is likely in the default state - this layout loads with the sidebar collapsed by default and may have different JavaScript behavior for toggling.

### Use Case
- Same as Sidebar Mini, but for applications that prefer to load with sidebar collapsed
- Power users who prefer maximum screen space by default
- Applications where sidebar is secondary to main content

---

## 9. Sidebar Mini + Logo Switch

**URL:** `layout/logo-switch.html`

### Body Classes
```
layout-fixed sidebar-expand-lg sidebar-mini bg-body-tertiary app-loaded hold-transition sidebar-collapse
```

### Behavior
- **Sidebar Width:** `73.5938px` - Collapsed to show only icons
- **Special Feature:** Logo changes between collapsed/expanded states

### Visual Effect
When the sidebar is collapsed, the logo/branding adapts to fit the narrow width (shows abbreviated version or icon only). When expanded, the full logo appears.

### Use Case
- Professional applications where branding must always be visible
- Dashboards that need to maintain brand identity in both states
- Applications with recognizable logo iconography

---

## 10. Layout RTL (Right-to-Left)

**URL:** `layout/layout-rtl.html`

### HTML Attributes
```html
<html dir="rtl" lang="en">
```

### Body Classes
```
layout-fixed sidebar-expand-lg sidebar-open bg-body-tertiary app-loaded hold-transition
```

### Behavior
- **Text Direction:** Right-to-left
- **Sidebar Position:** Right side of screen instead of left
- **All elements:** Mirrored horizontally
- **Key Attribute:** `dir="rtl"` on `<html>` element

### Visual Effect
The entire layout is mirrored:
- Sidebar appears on the right
- Text flows right-to-left
- Icons and navigation elements are reversed
- Breadcrumbs flow from right to left

### Use Case
- Arabic, Hebrew, Persian, Urdu language applications
- Localized applications for RTL language markets
- International applications requiring proper RTL support
- Accessibility requirements for RTL language users

---

## Key CSS Classes Summary

| Class | Purpose |
|-------|---------|
| `.layout-fixed` | Makes sidebar sticky/fixed |
| `.fixed-header` | Makes header sticky at top |
| `.fixed-footer` | Makes footer sticky at bottom |
| `.sidebar-mini` | Enables mini sidebar mode |
| `.sidebar-collapse` | Collapses sidebar to icon-only view |
| `.sidebar-expand-lg` | Sidebar expands at large breakpoint |
| `.sidebar-open` | Indicates sidebar is in open state |

---

## Implementation in Django MVP

Based on this analysis, Django MVP should:

1. **Provide configuration options** for each layout type via `MVP` settings dict
2. **Support dynamic body classes** through configuration
3. **Implement all 10 layout variations** as options in `mvp/base.html`
4. **Create component-level controls** for sidebar mini, logo switching, and custom areas
5. **Support RTL mode** through configuration and proper HTML attributes

### Recommended Configuration Structure

```python
MVP = {
    "layout": {
        "fixed_sidebar": True,      # .layout-fixed
        "fixed_header": False,       # .fixed-header
        "fixed_footer": False,       # .fixed-footer
        "sidebar_mini": False,       # .sidebar-mini
        "sidebar_collapsed": False,  # .sidebar-collapse
        "sidebar_expand": "lg",      # .sidebar-expand-{breakpoint}
        "rtl": False,                # dir="rtl" attribute
        "body_class": "",            # Additional custom classes
    },
    "custom_areas": {
        "top": None,     # Template path or block name
        "bottom": None,  # Template path or block name
    }
}
```

---

## Conclusion

AdminLTE 4 provides a comprehensive set of layout options that can be mixed and matched through CSS classes. The key insight is that these layouts are **additive** - classes like `.layout-fixed`, `.fixed-header`, and `.fixed-footer` can be combined to create hybrid layouts.

The most versatile layouts for admin dashboards are:
- **Fixed Complete** - For application-like experiences
- **Fixed Sidebar** - For navigation-heavy applications
- **Sidebar Mini** - For maximizing content space

All layouts maintain Bootstrap 5's responsive behavior and adapt appropriately to mobile viewports.
