# Inner Layout Component API Contract

**Component Name**: `inner` (used as `<c-page>`)
**Component Path**: `mvp/templates/cotton/inner/index.html`
**Version**: 1.0.0
**Status**: Implemented

## Component Purpose

Provides a CSS Grid-based nested layout structure within the outer AdminLTE 4 layout, offering four configurable areas: toolbar (top), footer (bottom), secondary sidebar (right), and main content (center).

Components are positioned using CSS Grid with specific classes:

- `<c-page.toolbar>` → `.page-toolbar` class → Grid Row 1
- `<c-page.sidebar>` → `.page-sidebar` class → Grid Column 2, Rows 2-3
- `<c-page.footer>` → `.page-footer` class → Grid Row 3
- Default slot content → `.page-layout-content` wrapper → Grid Row 2, Column 1

## Usage Syntax

```html
<c-page :toolbar_fixed="True" :footer_fixed="True" sidebar_breakpoint="lg" :sidebar_toggleable="True">
  <c-page.toolbar>
    <h2>Toolbar Title</h2>
    <c-slot name="end">
      <c-page.toolbar.widget icon="expand" />
    </c-slot>
  </c-page.toolbar>

  <!-- Required: Main content in default slot -->
  [Main content here]

  <c-page.sidebar collapsed>
    <!-- Optional: Sidebar content -->
  </c-page.sidebar>

  <c-page.footer>
    <small>Footer Content</small>
    <c-slot name="end">
      Additional footer content
    </c-slot>
  </c-page.footer>
</c-page>
```

**Note**: Sub-components use dot notation (`<c-page.toolbar>`, `<c-page.sidebar>`, `<c-page.footer>`) and are positioned via CSS Grid. The order of components in the markup doesn't matter - CSS Grid handles positioning. Use `:` prefix for boolean attributes (e.g., `:toolbar_fixed="True"`).

## Attributes

The `<c-page>` component accepts the following attributes:

### Main Component Attributes

| Attribute | Type | Default | Description |
| --- | --- | --- | --- |
| `toolbar_fixed` | boolean | `False` | Makes toolbar sticky to top when scrolling |
| `footer_fixed` | boolean | `False` | Makes footer sticky to bottom when scrolling |
| `sidebar_fixed` | boolean | `False` | Makes sidebar sticky when scrolling |
| `sidebar_breakpoint` | string | `"lg"` | Bootstrap breakpoint for sidebar visibility (`sm`, `md`, `lg`, `xl`, `xxl`) |
| `sidebar_toggleable` | boolean | `False` | Enables sidebar toggle functionality with collapse/expand button |
| `class` | string | `""` | Additional CSS classes for the wrapper div |

**Boolean Attributes**: Use `:` prefix for Python booleans: `:toolbar_fixed="True"` or `:sidebar_toggleable="False"`

**Sidebar Breakpoint**: Controls when sidebar is visible on responsive layouts. Default `"lg"` means sidebar appears on large screens (≥992px).

## Child Components

### `<c-page.toolbar>`

- **Component Path**: `mvp/templates/cotton/inner/toolbar.html`
- **Required**: No
- **Description**: Top toolbar area - sticky to top when `toolbar_fixed` is `True`
- **Grid Position**: Row 1, Columns 1-2 (spans all columns)
- **CSS Class**: `.page-toolbar` (with `.page-toolbar-fixed` when `toolbar_fixed="True"`)
- **Positioning**: `position: sticky; top: 0;` when fixed
- **Attributes**:
  - `collapsible` (boolean) - Adds a toggle button for sidebar collapse/expand
  - `class` (string) - Additional CSS classes
- **Slots**:
  - Default slot - Main toolbar content
  - `end` slot - Content positioned at the right end of toolbar
- **Example**:

  ```html
  <c-page.toolbar collapsible>
    <h2 class="mb-0">Page Title</h2>
    <c-slot name="end">
      <c-page.toolbar.widget icon="expand" />
    </c-slot>
  </c-page.toolbar>
  ```

### `<c-page.toolbar.widget>`

- **Component Path**: `mvp/templates/cotton/inner/toolbar/widget.html`
- **Required**: No
- **Description**: Pre-built toolbar action widget (e.g., expand/collapse button)
- **Attributes**:
  - `icon` (string) - Icon name for the widget
- **Example**:

  ```html
  <c-page.toolbar.widget icon="expand" />
  ```

### `<c-page.footer>`

- **Component Path**: `mvp/templates/cotton/inner/footer.html`
- **Required**: No
- **Description**: Bottom footer area - sticky to bottom when `footer_fixed` is `True`
- **Grid Position**: Row 3, Column 1
- **CSS Class**: `.page-footer` (with `.page-footer-fixed` when `footer_fixed="True"`)
- **Positioning**: `position: sticky; bottom: 0;` when fixed
- **Attributes**: None
- **Slots**:
  - Default slot - Main footer content
  - `end` slot - Content positioned at the right end of footer
- **Example**:

  ```html
  <c-page.footer>
    <small>Footer Content</small>
    <c-slot name="end">
      Text on the right
    </c-slot>
  </c-page.footer>
  ```

### `<c-page.sidebar>`

- **Component Path**: `mvp/templates/cotton/inner/sidebar.html`
- **Required**: No
- **Description**: Right sidebar area - spans content and footer rows, sticky when `sidebar_fixed` is `True`
- **Grid Position**: Rows 2-3, Column 2
- **CSS Class**: `.page-sidebar` (with `.page-sidebar-fixed` when `sidebar_fixed="True"`)
- **Scrolling**: Independently scrollable (overflow-y: auto)
- **Responsive**: Visibility controlled by parent's `sidebar_breakpoint` attribute (default: `lg` = 992px)
- **Attributes**:
  - `collapsed` (boolean) - Initial collapsed state (only relevant when `sidebar_toggleable="True"`)
- **Example**:

  ```html
  <c-page.sidebar collapsed>
    <div class="p-3">
      <h6>Sidebar Content</h6>
      <ul class="nav flex-column">
        <li class="nav-item"><a class="nav-link" href="#">Filter 1</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Filter 2</a></li>
      </ul>
    </div>
  </c-page.sidebar>
  ```

### Default Slot (Main Content)

- **Required**: Yes
- **Description**: Main content area - fills available space between toolbar and footer
- **Grid Position**: Row 2, Column 1
- **CSS Wrapper**: Content is placed in the default slot of the `.page-layout` wrapper
- **Scrolling**: Independently scrollable (overflow-y: auto)
- **Example**:

  ```html
  <c-page>
    <div class="p-4">
      <h2>Main Content</h2>
      <table class="table">...</table>
    </div>
  </c-page>
  ```

## HTML Output Structure

```html
<div class="page-layout sidebar-breakpoint-{{ sidebar_breakpoint }} {% if class %}{{ class }}{% endif %}"
     data-page-layout>

  <!-- Toolbar (if <c-page.toolbar> component present) -->
  <header class="page-toolbar{% if toolbar_fixed %} page-toolbar-fixed{% endif %}"
          role="banner"
          aria-label="Page toolbar">
    {% if toolbar has collapsible attribute %}
      <button type="button"
              class="btn btn-sm btn-outline-secondary page-layout-toggle-btn"
              aria-expanded="true"
              aria-controls="page-sidebar"
              aria-label="Toggle sidebar"
              data-page-layout-toggle>
        <span class="toggle-icon-close" aria-hidden="true">
          <c-icon name="arrow-right" />
        </span>
        <span class="toggle-icon-open" aria-hidden="true">
          <c-icon name="arrow-right" />
        </span>
      </button>
    {% endif %}
    <!-- <c-page.toolbar> default slot content rendered here -->
    <!-- <c-page.toolbar> 'end' slot content rendered at right -->
  </header>

  <!-- Main Content (default slot) -->
  {{ slot }}

  <!-- Sidebar (if <c-page.sidebar> component present) -->
  <aside id="page-sidebar"
         class="page-sidebar{% if sidebar_fixed %} page-sidebar-fixed{% endif %}"
         role="complementary"
         aria-label="Sidebar content">
    <!-- <c-page.sidebar> content rendered here -->
  </aside>

  <!-- Footer (if <c-page.footer> component present) -->
  <footer class="page-footer{% if footer_fixed %} page-footer-fixed{% endif %}"
          role="contentinfo"
          aria-label="Page footer">
    <!-- <c-page.footer> default slot content rendered here -->
    <!-- <c-page.footer> 'end' slot content rendered at right -->
  </footer>
</div>
```

**Component Detection**: The `<c-page>` component (via `inner/index.html`) uses Cotton's dot-notation architecture. Sub-components (`<c-page.toolbar>`, `<c-page.sidebar>`, `<c-page.footer>`) are separate template files in the `inner/` folder that are automatically positioned by CSS Grid via their respective classes (`.page-toolbar`, `.page-sidebar`, `.page-footer`).

## CSS Grid Structure

The inner layout uses CSS Grid with the following structure, **mirroring AdminLTE 4's app-wrapper pattern**:

### Inner Layout Grid

```css
.page-layout {
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-rows: min-content 1fr min-content;
  grid-template-areas:
    "toolbar sidebar"
    "main sidebar"
    "footer sidebar";
  height: 100%;
  gap: 0;
}
```

### AdminLTE 4 Outer Layout Grid (for comparison)

```scss
.app-wrapper {
  display: grid;
  grid-template-columns: auto 1fr;  // Sidebar first, then main content
  grid-template-rows: min-content 1fr min-content;
  grid-template-areas:
    "app-sidebar app-header"
    "app-sidebar app-main"
    "app-sidebar app-footer";
  min-height: 100vh;
  gap: 0;
}
```

**Key Similarities:**

- Both use CSS Grid with named grid areas
- Both use `min-content 1fr min-content` for rows (header/footer collapse when absent, main content fills)
- Both use auto-width columns for sidebar (collapses to 0 when hidden)
- Both use `gap: 0` for no spacing between grid areas

**Key Differences:**

- Inner layout: Sidebar on **right** (column 2), content first
- Outer layout: Sidebar on **left** (column 1), sidebar first
- Inner layout: Fixed `height: 100%` (fills container)
- Outer layout: `min-height: 100vh` (fills viewport)

**Design Decisions:**

- **Columns**: `1fr auto` - Main content expands to fill space, sidebar takes auto width (collapses to 0 when hidden)
- **Rows**: `min-content 1fr min-content` - Toolbar/footer take minimum needed height, main content fills remaining space (rows collapse when elements not present in DOM)
- **Grid Areas**: Named areas for explicit positioning via `grid-area` property
- **Height**: 100% to fill container

### Grid Area Assignments

- `.toolbar` → `grid-area: toolbar` (Row 1, spans columns 1-2)
- `.main` → `grid-area: main` (Row 2, Column 1)
- `.sidebar` → `grid-area: sidebar` (Rows 1-3, Column 2 - spans all rows)
- `.footer` → `grid-area: footer` (Row 3, Column 1)

### CSS Classes Applied

#### Container Classes

- `.page-layout` - Main grid container with CSS Grid layout
- `.sidebar-breakpoint-{breakpoint}` - Applied based on `sidebar_breakpoint` attribute (`sm`, `md`, `lg`, `xl`, `xxl`)
- Custom classes from `class` attribute are added to the wrapper

#### Sub-Component Classes

- `.page-toolbar` - Toolbar area (header element, `grid-area: toolbar`)
- `.page-toolbar-fixed` - Applied when `toolbar_fixed="True"` (adds `position: sticky; top: 0`)
- `.page-footer` - Footer area (footer element, `grid-area: footer`)
- `.page-footer-fixed` - Applied when `footer_fixed="True"` (adds `position: sticky; bottom: 0`)
- `.page-sidebar` - Secondary sidebar (aside element, `grid-area: sidebar`)
- `.page-sidebar-fixed` - Applied when `sidebar_fixed="True"` (adds `position: sticky`)
- `.page-layout-toggle-btn` - Toggle button in toolbar (when `collapsible` attribute present)

#### Sticky Positioning (AdminLTE 4 Pattern)

**AdminLTE 4 uses wrapper classes to control sticky behavior:**

```scss
// AdminLTE 4 outer layout
.fixed-header {
  .app-header {
    position: sticky;
    top: 0;
    z-index: $lte-zindex-fixed-header;
  }
}

.fixed-footer {
  .app-footer {
    position: sticky;
    bottom: 0;
    z-index: $lte-zindex-fixed-footer;
  }
}
```

**Inner layout follows same pattern with attributes:**

```scss
// Applied when toolbar_fixed="True"
.page-toolbar-fixed {
  position: sticky;
  top: 0;
  z-index: 100;
}

// Applied when footer_fixed="True"
.page-footer-fixed {
  position: sticky;
  bottom: 0;
  z-index: 100;
}

// Applied when sidebar_fixed="True"
.page-sidebar-fixed {
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow-y: auto;
}
```

**Key Points:**

- Sticky positioning is **opt-in** via attributes, not default
- Uses same `position: sticky` + `top: 0` / `bottom: 0` pattern as AdminLTE 4
- Z-index ensures proper layering (toolbar/footer above content)
- Sidebar sticky is top-aligned with scroll overflow

```css
.sidebar.sidebar-collapse {
  min-width: 0;
  max-width: 0;
  width: 0;
  padding: 0;
  border: 0;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
  transition: all 0.3s ease;
}
```

When sidebar is collapsed, the grid's `auto` column width naturally shrinks to 0, allowing main content to expand.

#### Responsive Behavior

Below the configured breakpoint, the sidebar becomes fixed-positioned and slides in from the right:

```css
@media (max-width: 991px) { /* for sidebar-breakpoint-lg */
  .sidebar {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 1050;
    transform: translateX(100%);
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
  }

  .sidebar.sidebar-open {
    transform: translateX(0);
  }
}
```

### Data Attributes

- `[data-page-layout]` - Applied to wrapper for JavaScript targeting
- `[data-page-layout-toggle]` - Applied to toggle button

## CSS Variables

The component uses CSS custom properties for layout configuration (defined in `_page-layout.scss`):

- Layout configuration is handled entirely via CSS classes and SCSS
- Responsive breakpoints are controlled by `sidebar_breakpoint` attribute which adds corresponding class
- Customization via standard CSS/SCSS overrides

## JavaScript

The component uses JavaScript (`mvp/static/mvp/js/page-layout.js`) for:

- **Sidebar toggle functionality** - When `sidebar_toggleable="True"` and toolbar has `collapsible` attribute
- **Session persistence** - Toggle state saved in sessionStorage
- **ARIA state management** - Updates `aria-expanded` on toggle button

JavaScript is loaded automatically by the Django MVP package and activates when `[data-page-layout-toggle]` elements are detected.

## Accessibility

### ARIA Attributes

- Toolbar: `role="region"` `aria-label="Page toolbar"`
- Footer: `role="contentinfo"` `aria-label="Page footer"`
- Sidebar: `role="complementary"` `aria-label="Secondary sidebar"`
- Toggle: `aria-label="Toggle sidebar"` `aria-expanded="true/false"` `aria-controls="page-sidebar"`

### Keyboard Navigation

- All interactive elements are keyboard-accessible
- Toggle button responds to Enter and Space keys
- Tab order: toolbar → content → sidebar → footer

## Examples

### Minimal Usage (Content Only)

```html
<c-page>
  <div class="p-4">
    <h1>My Content</h1>
    <p>Simple page content without toolbar, footer, or sidebar.</p>
  </div>
</c-page>
```

### With Toolbar and Footer

```html
<c-page :toolbar_fixed="True" :footer_fixed="True">
  <c-page.toolbar>
    <div class="d-flex justify-content-between align-items-center p-3">
      <h2>Data Table</h2>
      <button class="btn btn-primary">Export</button>
    </div>
  </c-page.toolbar>

  <table class="table">
    <thead><tr><th>Name</th><th>Email</th></tr></thead>
    <tbody>
      <tr><td>John</td><td>john@example.com</td></tr>
    </tbody>
  </table>

  <c-page.footer>
    <div class="p-3 text-center">
      <span>Page 1 of 10</span>
    </div>
  </c-page.footer>
</c-page>
```

### Full Layout with Sidebar and Toggle

```html
<c-page :toolbar_fixed="True" :footer_fixed="True" :sidebar_toggleable="True" sidebar_breakpoint="lg">

  <c-page.toolbar collapsible>
    <h2 class="mb-0">Dashboard</h2>
    <c-slot name="end">
      <c-page.toolbar.widget icon="expand" />
      <button class="btn btn-sm btn-primary">Actions</button>
    </c-slot>
  </c-page.toolbar>

  <!-- Main content -->
  <div class="container-fluid p-4">
    <div class="row">
      <div class="col-md-6">
        <c-small-box title="Users" value="150" />
      </div>
      <div class="col-md-6">
        <c-small-box title="Sales" value="$1,234" />
      </div>
    </div>
  </div>

  <c-page.sidebar collapsed>
    <div class="p-3">
      <h6>Filters</h6>
      <form>
        <div class="mb-3">
          <label class="form-label">Status</label>
          <select class="form-select">
            <option>All</option>
            <option>Active</option>
            <option>Inactive</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary w-100">Apply</button>
      </form>
    </div>
  </c-page-sidebar>

  <c-page-footer class="bg-light border-top">
    <div class="d-flex justify-content-between align-items-center p-3">
      <span>Last updated: Jan 19, 2026</span>
      <button class="btn btn-sm btn-secondary">Refresh</button>
    </div>
  </c-page-footer>
</c-page-layout>
```

### Without Sidebar

```html
<c-page-layout>

  <c-page-toolbar>
    <h2 class="p-3">Wide Layout</h2>
  </c-page-toolbar>

  <div class="p-4">
    Content spans full width - no sidebar component included
  </div>
</c-page-layout>
```

## Validation & Error Handling

### Required Validations

1. **Default slot must have content**: If empty, layout renders but may appear broken

### Error States

- **No Content**: Layout renders but appears empty (valid state)
- **Missing Child Component**: If a child component (`<c-page-toolbar>`, etc.) is not included, that area simply doesn't render

## Testing Requirements

### Unit Tests

```python
def test_page_layout_basic_rendering(rf):
    """Test basic inner layout with default slot only"""

def test_page_layout_with_toolbar_footer(rf):
    """Test layout with toolbar and footer slots"""

def test_page_layout_sidebar_visible(rf):
    """Test sidebar visibility with attribute"""

def test_page_layout_custom_classes(rf):
    """Test custom CSS classes applied"""

def test_page_layout_sidebar_hidden(rf):
    """Test sidebar hidden when sidebar_visible='false'"""
```

### Integration Tests

```python
def test_page_layout_within_outer_layout(client):
    """Test inner layout renders correctly within mvp/base.html"""

def test_page_layout_no_conflict_with_outer(client):
    """Test no CSS/JS conflicts with outer layout"""
```

### E2E Tests (Playwright)

```python
def test_toolbar_sticky_on_scroll(page):
    """Verify toolbar sticks to top when scrolling"""

def test_footer_sticky_on_scroll(page):
    """Verify footer sticks to bottom when scrolling"""

def test_sidebar_responsive_hiding(page):
    """Verify sidebar hides below breakpoint (992px)"""

def test_independent_scrolling(page):
    """Verify content and sidebar scroll independently"""
```

## Compatibility

### Django Versions

- Django 4.2+
- Django 5.0+

### Django Cotton Versions

- django-cotton >= 2.3.1

### Browser Support

- Modern browsers with CSS Grid support (95%+ global)
- CSS Grid: Chrome 57+, Firefox 52+, Safari 10.1+, Edge 16+
- CSS Sticky: Chrome 56+, Firefox 32+, Safari 13+, Edge 16+

### Bootstrap Version

- Bootstrap 5.3

## Deprecation Policy

No deprecations planned. This is the initial version.

## Changelog

### Version 1.0.0 (2026-01-19)

- Initial design and API specification
- CSS Grid-based layout structure
- Four configurable areas: toolbar, content, footer, sidebar
- Template-driven configuration via component attributes
- Optional user toggle for sidebar visibility
- SessionStorage persistence for toggle state
