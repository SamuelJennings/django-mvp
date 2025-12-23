# Structure and Naming Conventions

This document defines the structural elements and naming conventions used throughout Django Cotton Layouts.

## Layout Hierarchy

Django Cotton Layouts uses a nested flex-based layout system with three levels of structure:

### Level 1: Outer Layout (Application Shell)
### Level 2: Main Content Area (Page Container)  
### Level 3: Inner Layout (Content Organization)

---

## Level 1: Outer Layout (Application Shell)

The **Outer Layout** forms the application shell and is defined in `layouts/standard.html`.

### Structure Elements

```
.app-shell (body wrapper)
├── .site-sidebar (left navigation, collapsible)
├── .app-column (main application area)
    ├── .site-navbar (top navigation)
    ├── .app-main (primary content container)
    └── .app-footer (bottom footer, optional)
```

### Class Names & Purpose

| Class | Element | Purpose | Responsive Behavior |
|-------|---------|---------|---------------------|
| `.app-shell` | `<div>` | Root layout container using flexbox | Full viewport height |
| `.site-sidebar` | `<aside>` | Site-level navigation sidebar | Toggles to offcanvas on mobile |
| `.app-column` | `<div>` | Main column containing navbar, content, and footer | Flex column, fills remaining space |
| `.site-navbar` | `<nav>` | Top navigation bar | Sticky or static based on config |
| `.app-main` | `<main>` | Primary content container | Scrollable, flex: 1 |
| `.app-footer` | `<footer>` | Application footer | Sticky or flow based on config |

### Configuration

```python
PAGE_CONFIG = {
    "layout": "sidebar",  # or "navbar" or "both"
    "navigation": {
        "toggle_at": "lg",  # Breakpoint for sidebar offcanvas
        "collapsible": True,
    },
    "footer": {
        "sticky": True,  # Stick to bottom
        "sticky_breakpoint": "md",  # Stick only on mobile, flow on desktop
    }
}
```

---

## Level 2: Main Content Area (Page Container)

The **Main Content Area** (`.app-main`) contains page-level elements like toolbars, breadcrumbs, and titles.

### Structure Elements

```
.app-main
├── .page-toolbar (action buttons, filters, optional)
├── .page-breadcrumbs (navigation breadcrumbs, optional)
├── .page-header (page title and metadata)
│   ├── .page-title
│   ├── .page-subtitle (optional)
│   └── .page-actions (header action buttons)
└── .page-content (main page content area)
```

### Class Names & Purpose

| Class | Element | Purpose | Used In |
|-------|---------|---------|---------|
| `.page-toolbar` | `<div>` | Top toolbar for page-level actions | List views, filter controls |
| `.page-breadcrumbs` | `<nav>` | Breadcrumb navigation | All page types |
| `.page-header` | `<header>` | Page title section | All page types |
| `.page-title` | `<h1>` | Main page title | All page types |
| `.page-subtitle` | `<p>` | Optional subtitle/description | Detail views |
| `.page-actions` | `<div>` | Action buttons in header | Detail/list views |
| `.page-content` | `<div>` | Main content area | All page types |

### Template Usage

These elements are used in specialized layout templates:
- `layouts/list_view.html` - List view pattern
- `layouts/detail_view.html` - Detail view pattern  
- `layouts/form_view.html` - Form view pattern

---

## Level 3: Inner Layout (Content Organization)

The **Inner Layout** organizes content within `.page-content` using an optional dual-sidebar pattern.

### Structure Elements

```
.content-shell (inner flex container)
├── .content-sidebar-left (primary sidebar, optional, collapsible)
├── .content-main (central content area)
└── .content-sidebar-right (secondary sidebar, optional, collapsible)
```

### Class Names & Purpose

| Class | Element | Purpose | Responsive Behavior |
|-------|---------|---------|---------------------|
| `.content-shell` | `<div>` | Inner layout flex container | Horizontal flex on desktop, stacks on mobile |
| `.content-sidebar-left` | `<aside>` | Primary (left) sidebar for navigation/filters | Collapsible, min-width when collapsed |
| `.content-main` | `<div>` | Central content area | Flex: 1, scrollable |
| `.content-sidebar-right` | `<aside>` | Secondary (right) sidebar for metadata/tools | Collapsible, min-width when collapsed |

### Toggle Buttons

| Class | Purpose |
|-------|---------|
| `.content-sidebar-toggle-left` | Toggle button for left sidebar |
| `.content-sidebar-toggle-right` | Toggle button for right sidebar |

### Visibility Classes

| Class | Behavior |
|-------|----------|
| `.visible-expanded` | Show only when sidebar is expanded |
| `.visible-collapsed` | Show only when sidebar is collapsed |

### Configuration via CSS Variables

```css
:root {
  /* Left sidebar */
  --content-sidebar-left-width: 280px;
  --content-sidebar-left-max-width: 320px;
  --content-sidebar-left-min-width: 60px;
  
  /* Right sidebar */
  --content-sidebar-right-width: 280px;
  --content-sidebar-right-max-width: 320px;
  --content-sidebar-right-min-width: 60px;
  
  /* Backgrounds and borders */
  --content-sidebar-bg: #fafafa;
  --content-sidebar-border: #e5e7eb;
}
```

---

## Component Naming Patterns

### Sidebar Components

| Component | Class | Purpose |
|-----------|-------|---------|
| Wrapper | `.sidebar` | Base sidebar class (used for both site and content sidebars) |
| Container | `.sidebar-content` | Inner content wrapper |
| Header | `.sidebar-header` | Top section (logo, branding) |
| Body | `.sidebar-body` | Main scrollable area |
| Footer | `.sidebar-footer` | Bottom section (user profile, settings) |
| Menu Item | `.menu-item` | Individual menu links |
| Menu Text | `.menu-text` | Text content in menu items |
| Menu Icon | `.menu-icon` | Icon in menu items |
| Menu Heading | `.menu-heading` | Section headings in sidebar |

### State Classes

| Class | Scope | Behavior |
|-------|-------|----------|
| `.collapsed` | Site sidebar, content sidebars | Applied when sidebar is collapsed |
| `.expanded` | Site sidebar, content sidebars | Default state (can be explicit) |
| `.offcanvas-{breakpoint}` | Site sidebar | Bootstrap offcanvas behavior |

---

## JavaScript Variable Naming

### Site Sidebar

```javascript
// Storage keys
const SITE_SIDEBAR_COLLAPSED_KEY = 'siteSidebarCollapsed'

// DOM selectors
const siteSidebar = document.querySelector('.site-sidebar')
const siteSidebarToggle = document.querySelector('.sidebar-toggle')
```

### Content Sidebars

```javascript
// Storage keys  
const CONTENT_SIDEBAR_LEFT_KEY = 'contentSidebarLeftCollapsed'
const CONTENT_SIDEBAR_RIGHT_KEY = 'contentSidebarRightCollapsed'

// DOM selectors
const contentSidebarLeft = document.querySelector('.content-sidebar-left')
const contentSidebarRight = document.querySelector('.content-sidebar-right')
const toggleLeft = document.querySelector('.content-sidebar-toggle-left')
const toggleRight = document.querySelector('.content-sidebar-toggle-right')
```

---

## SCSS File Organization

| File | Purpose | Key Classes |
|------|---------|-------------|
| `_outer-layout.scss` | Outer layout (app shell) | `.app-shell`, `.site-sidebar`, `.app-column`, `.app-main`, `.app-footer` |
| `_sidebar.scss` | Sidebar component (all types) | `.sidebar`, `.sidebar-content`, `.menu-item` |
| `_navbar.scss` | Navbar component | `.site-navbar`, navbar variants |
| `_page.scss` | Page-level elements | `.page-toolbar`, `.page-header`, `.page-title`, `.page-content` |
| `_content-layout.scss` | Inner content layout | `.content-shell`, `.content-sidebar-left`, `.content-sidebar-right`, `.content-main` |

---

## Migration from Old Names

For backwards compatibility during migration:

| Old Class | New Class | Status |
|-----------|-----------|--------|
| `.sidebar-layout` | `.app-shell` | Aliased |
| `.main-column` | `.app-column` | Aliased |
| `.main-content` | `.app-main` | Aliased |
| `.inner-layout` | `.content-shell` | Aliased |
| `.inner-primary` | `.content-sidebar-left` | Aliased |
| `.inner-secondary` | `.content-sidebar-right` | Aliased |
| `.inner-main` | `.content-main` | Aliased |

---

## Design Principles

1. **Semantic Naming**: Names describe purpose and location, not appearance
2. **Consistent Prefixes**: 
   - `app-*` for application shell elements
   - `site-*` for site-level navigation  
   - `page-*` for page-level elements
   - `content-*` for content area elements
3. **Level Clarity**: Names indicate hierarchy level (app → page → content)
4. **Responsive Suffixes**: Use Bootstrap breakpoints (e.g., `-md`, `-lg`)
5. **State Classes**: Simple, semantic (`.collapsed`, `.expanded`, `.active`)

---

## CSS Variable Naming

Follow this pattern: `--{scope}-{component}-{property}`

Examples:
```css
/* Outer layout */
--app-sidebar-width: 280px;
--app-footer-height: 60px;

/* Site components */
--site-sidebar-bg: #ffffff;
--site-navbar-height: 60px;

/* Page elements */
--page-toolbar-height: 56px;
--page-header-padding: 1.5rem;

/* Content layout */
--content-sidebar-left-width: 280px;
--content-sidebar-right-width: 280px;
--content-main-padding: 1.5rem;
```

---

## Best Practices

### For Template Authors

1. Use semantic class names that describe purpose, not presentation
2. Follow the three-level hierarchy (app → page → content)
3. Use CSS variables for dimensions and colors
4. Provide responsive alternatives using visibility classes
5. Document custom components in this file

### For Theme Authors

1. Override CSS variables, not class definitions
2. Use the documented class names for custom styles
3. Test across all three layout levels
4. Ensure responsive behavior is maintained
5. Document theme-specific variables

### For JavaScript Developers

1. Use data attributes for configuration
2. Namespace localStorage keys by scope
3. Use semantic selectors (`.site-sidebar`, not `.sidebar:first`)
4. Preserve state across page loads
5. Handle mobile/desktop transitions gracefully
