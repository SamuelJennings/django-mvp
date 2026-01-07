# Research: AdminLTE Layout Component Separation

**Feature**: 001-layout-components
**Date**: January 5, 2026
**Status**: Complete

## Research Questions & Findings

### 1. AdminLTE 4 Layout Architecture

**Question**: What is the structure of AdminLTE's grid-based layout and how are components organized?

**Findings**:

AdminLTE 4 uses CSS Grid for layout with the `.app-wrapper` as the root container:

```scss
.app-wrapper {
  display: grid;
  grid-template-areas:
    "app-sidebar app-header"
    "app-sidebar app-main"
    "app-sidebar app-footer";
  grid-template-rows: min-content 1fr min-content;
  grid-template-columns: auto 1fr;
  min-height: 100vh;
}
```

**Component Areas**:

- **app-wrapper**: Root grid container
- **app-header**: Top navigation bar (min-content height, spans right column)
- **app-sidebar**: Left navigation (auto width, spans all rows)
- **app-main**: Main content area (1fr height, flexible)
- **app-footer**: Footer (min-content height, spans right column)

**Key CSS Classes**:

- Layout modifiers: `layout-fixed`, `sidebar-expand-{breakpoint}`
- Component-specific: `navbar`, `sidebar-brand`, `app-content-header`, `app-content`
- Theme options: `bg-body-secondary`, `data-bs-theme="dark"`

**Decision**: Each component must render its designated grid area with exact CSS class structure.

---

### 2. Cotton Component Best Practices

**Question**: What are the patterns for defining Cotton components with c-vars and slots?

**Findings**:

**c-vars Declaration**:

```django
<c-vars
  title="Default Title"
  show_footer="True"
  class
/>
```

- Declare all accepted attributes with defaults
- String values in quotes, boolean values without quotes
- Empty string default for optional CSS classes

**Slot System**:

```django
{# Default slot - main content #}
{{ slot }}

{# Named slots - specific sections #}
{{ header }}
{{ footer }}

{# Conditional rendering #}
{% if footer %}
  <div class="footer">{{ footer }}</div>
{% endif %}
```

**Naming Convention**:

- Components: snake-case filenames (e.g., `wrapper.html`, `app_header.html`)
- Usage: `<c-app />` or `<c-app.header />`
- Attributes: snake_case (e.g., `fixed_sidebar="True"`)

**Decision**: All components will use c-vars for configuration, default slot for main content, and named slots for specific sections.

---

### 3. Current mvp/base.html Analysis

**Question**: What blocks exist and how can we maintain backward compatibility?

**Findings**:

**Current Block Structure**:

```django
{% block app_header %}
  {% block navbar_left %}{% endblock %}
  {% block navbar_right %}{% endblock %}
{% endblock %}

{% block app_sidebar %}
  {% block sidebar_menu %}{% endblock %}
{% endblock %}

{% block page_header %}
  {% block page_title %}{% endblock %}
  {% block breadcrumbs %}{% endblock %}
{% endblock %}

{% block content %}{% endblock %}

{% block app_footer %}
  {% block footer_right %}{% endblock %}
{% endblock %}
```

**MVP Settings Usage**:

- `{{ mvp.brand.text }}` - sidebar brand text
- `{{ mvp.brand.logo }}` - sidebar brand logo
- `{{ mvp.footer.visible }}` - footer visibility toggle
- `{{ mvp.footer.text }}` - footer text

**Backward Compatibility Strategy**:

1. Keep all existing blocks in mvp/base.html
2. Blocks now wrap component invocations instead of HTML
3. Component attributes can be overridden via block override
4. MVP settings no longer used (deferred to future)

**Decision**: mvp/base.html will use the new components while preserving all block names and positions.

---

## Component Interface Design

### Wrapper Component

**File**: `mvp/templates/cotton/app/wrapper.html`

**Attributes** (c-vars):

- `body_class` - Additional classes for body element
- `fixed_sidebar="False"` - Enable fixed sidebar layout
- `sidebar_expand="lg"` - Breakpoint for sidebar expansion

**Slots**:

- `header` - App header content
- `sidebar` - App sidebar content
- `main` - Main content area
- `footer` - Footer content (optional)

---

### Header Component

**File**: `mvp/templates/cotton/app/header.html`

**Attributes** (c-vars):

- `class` - Additional classes for header
- `container_class="container-fluid"` - Container class

**Slots**:

- `left` - Left navbar items
- `right` - Right navbar items

---

### Sidebar Component

**File**: `mvp/templates/cotton/app/sidebar.html`

**Attributes** (c-vars):

- `brand_text="Django MVP"` - Brand text
- `brand_logo=""` - Brand logo URL
- `brand_url="/"` - Brand link URL
- `theme="dark"` - Sidebar theme (dark/light)
- `class="bg-body-secondary"` - Additional classes

**Slots**:

- Default slot - Sidebar menu content

---

### Main Component

**File**: `mvp/templates/cotton/app/main.html`

**Attributes** (c-vars):

- `show_header="True"` - Show content header section
- `container_class="container-fluid"` - Container class

**Slots**:

- `header` - Page header content (title/breadcrumbs)
- Default slot - Main content

---

### Footer Component

**File**: `mvp/templates/cotton/app/footer.html`

**Attributes** (c-vars):

- `text="Copyright &copy; 2026"` - Footer text
- `class` - Additional classes

**Slots**:

- `right` - Right-aligned content
- Default slot - Main footer content

---

## Alternatives Considered

### Alternative 1: Keep MVP Settings Integration

**Approach**: Components read from mvp context directly

**Rejected Because**:

- Less flexible - global settings limit per-page customization
- User explicitly requested deferring settings integration
- Component attributes provide better reusability

### Alternative 2: Single Monolithic Component

**Approach**: One component with many conditional sections

**Rejected Because**:

- Violates separation of concerns
- Prevents selective overriding
- Makes testing more complex
- Doesn't meet FR-001 requirement for separation

### Alternative 3: Deep Component Nesting

**Approach**: Wrapper contains header, header contains navbar, etc.

**Rejected Because**:

- Cotton components don't support deep nesting well
- Makes override syntax verbose
- Complicates slot passing between layers

---

## Technology Decisions

### Decision 1: Cotton c-vars Over Context Variables

**Rationale**: More explicit, better IDE support, self-documenting components

### Decision 2: Named Slots Over Numbered Slots

**Rationale**: Clearer intent, easier to maintain, better DX

### Decision 3: Separate app/ Directory

**Rationale**: Clear distinction between layout components (app/) and widget components (adminlte/)

---

## Testing Strategy

**Component-Level Tests**:

- Render each component with various attribute combinations
- Verify correct HTML structure and CSS classes
- Test slot content injection
- Test default value application

**Integration Tests**:

- Test mvp/base.html with new components
- Verify backward compatibility with existing blocks
- Test composition of subset of components

**Coverage Target**: 90%+ for component logic
