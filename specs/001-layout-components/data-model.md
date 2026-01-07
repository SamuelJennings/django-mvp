# Data Model: AdminLTE Layout Components

**Feature**: 001-layout-components
**Date**: January 5, 2026

## Overview

This feature does not introduce database models. Instead, it defines component interfaces (attributes, slots, and output structure) for the five AdminLTE layout Cotton components.

## Component Schemas

### 1. Wrapper Component

**Purpose**: Root grid container for AdminLTE layout

**Attributes**:

| Name | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `body_class` | string | `""` | No | Additional CSS classes for wrapper div |
| `fixed_sidebar` | boolean | `False` | No | Enable fixed sidebar layout (adds `layout-fixed` class) |
| `sidebar_expand` | string | `"lg"` | No | Breakpoint for sidebar expansion (sm/md/lg/xl/xxl) |

**Slots**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `header` | named | No | App header/navbar component |
| `sidebar` | named | No | App sidebar navigation component |
| `main` | named | Yes | Main content area component |
| `footer` | named | No | Footer component |

**Output Structure**:

```html
<div class="app-wrapper {{ body_class }}">
  {{ header }}
  {{ sidebar }}
  {{ main }}
  {{ footer }}
</div>
```

**Validation Rules**:

- `sidebar_expand` must be one of: sm, md, lg, xl, xxl
- At least one slot must have content
- `fixed_sidebar` is applied via class modification

---

### 2. Header Component

**Purpose**: Top navigation bar

**Attributes**:

| Name | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `class` | string | `""` | No | Additional CSS classes for nav element |
| `container_class` | string | `"container-fluid"` | No | Container div class |

**Slots**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `left` | named | No | Left navbar items (typically menu toggle) |
| `right` | named | No | Right navbar items (user menu, notifications) |

**Output Structure**:

```html
<nav class="app-header navbar navbar-expand bg-body {{ class }}">
  <div class="{{ container_class }}">
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" data-lte-toggle="sidebar" href="#" role="button">
          <i class="bi bi-list"></i>
        </a>
      </li>
      {{ left }}
    </ul>
    <ul class="navbar-nav ms-auto">
      {{ right }}
    </ul>
  </div>
</nav>
```

**Validation Rules**:

- Always includes sidebar toggle button
- Left and right slots are optional

---

### 3. Sidebar Component

**Purpose**: Left navigation sidebar

**Attributes**:

| Name | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `brand_text` | string | `"Django MVP"` | No | Brand/logo text |
| `brand_logo` | string | `""` | No | Brand logo image URL |
| `brand_url` | string | `"/"` | No | Brand link destination |
| `theme` | string | `"dark"` | No | Sidebar theme (dark/light) |
| `class` | string | `"bg-body-secondary"` | No | Additional CSS classes |

**Slots**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| (default) | default | No | Sidebar menu content |

**Output Structure**:

```html
<aside class="app-sidebar {{ class }} shadow" data-bs-theme="{{ theme }}">
  <div class="sidebar-brand">
    <a href="{{ brand_url }}" class="brand-link">
      {% if brand_logo %}
        <img src="{{ brand_logo }}" alt="{{ brand_text }}" class="brand-image" />
      {% endif %}
      <span class="brand-text fw-light">{{ brand_text }}</span>
    </a>
  </div>
  <div class="sidebar-wrapper">
    <nav class="mt-2">
      <ul class="nav sidebar-menu flex-column"
          data-lte-toggle="treeview"
          role="menu"
          data-accordion="false">
        {{ slot }}
      </ul>
    </nav>
  </div>
</aside>
```

**Validation Rules**:

- `theme` must be one of: dark, light
- `brand_logo` is optional; when empty, only text is shown
- Default slot content goes inside ul.sidebar-menu

---

### 4. Main Component

**Purpose**: Main content area with optional header

**Attributes**:

| Name | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `show_header` | boolean | `True` | No | Show content header section (title/breadcrumbs) |
| `container_class` | string | `"container-fluid"` | No | Container div class |

**Slots**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `header` | named | No | Page header content (title, breadcrumbs) |
| (default) | default | Yes | Main page content |

**Output Structure**:

```html
<main class="app-main">
  {% if show_header %}
    <div class="app-content-header">
      <div class="{{ container_class }}">
        {{ header }}
      </div>
    </div>
  {% endif %}
  <div class="app-content">
    {{ slot }}
  </div>
</main>
```

**Validation Rules**:

- Default slot is required (main content)
- Header slot only rendered if `show_header` is True
- Empty header slot with `show_header=True` renders empty header div

---

### 5. Footer Component

**Purpose**: Footer section with copyright and optional right content

**Attributes**:

| Name | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `text` | string | `"Copyright &copy; 2026"` | No | Main footer text (HTML allowed) |
| `class` | string | `""` | No | Additional CSS classes |

**Slots**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `right` | named | No | Right-aligned content |
| (default) | default | No | Replaces default text if provided |

**Output Structure**:

```html
<footer class="app-footer {{ class }}">
  <div class="float-end d-none d-sm-inline">
    {{ right }}
  </div>
  <strong>
    {% if slot %}
      {{ slot }}
    {% else %}
      {{ text }}
    {% endif %}
  </strong>
</footer>
```

**Validation Rules**:

- `text` can contain HTML entities and tags
- Default slot overrides `text` attribute if provided
- Right slot is optional

---

## Relationships

Component composition hierarchy (not parent-child, but recommended usage):

```
wrapper
├── header
│   ├── left slot
│   └── right slot
├── sidebar
│   └── (menu items)
├── main
│   ├── header slot (optional)
│   └── content slot
└── footer (optional)
    ├── (main text)
    └── right slot
```

**Constraints**:

- Wrapper is required - it establishes the grid layout
- Main is required - must have content area
- Header, sidebar, footer are optional for flexible layouts
- Components do not enforce child relationships (loose coupling)

---

## State Management

**No state**: All components are stateless templates. Configuration is passed via attributes each render.

**CSS State**: AdminLTE JavaScript may add classes (e.g., sidebar-collapse) - components must preserve these

---

## Compatibility

**Backward Compatibility**: Components must render HTML identical to current mvp/base.html structure when using default attributes.

**Migration Path**:

1. Current: monolithic base.html with blocks
2. Phase 1: base.html uses components with blocks wrapping component invocations
3. Future: Direct component usage in view templates
