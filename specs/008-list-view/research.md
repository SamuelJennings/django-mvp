# Research: Dashboard List View Mixin

**Feature**: 008-dash-list-view
**Date**: February 4, 2026

## Research Questions Resolved

### 1. Multi-Word Search Operator Behavior

**Question**: How should multi-word search queries be handled?

**Decision**: OR matching (any word matches)

**Rationale**: OR matching provides better user experience by showing more results, reducing "no results" scenarios. Users can refine with filters/sorting. This is the pattern used by most modern search interfaces.

**Implementation**: Split search term by whitespace, apply OR across all words and all fields.

### 2. Ordering Control UI Widget

**Question**: What UI widget should be used for ordering controls?

**Decision**: Dropdown menu (compact, single selection)

**Rationale**: Dropdown menus are space-efficient (critical for headers with multiple widgets), familiar to users, and work well on mobile devices. They can display field labels clearly and handle multiple sort options without cluttering the UI.

**Implementation**: Already implemented in `c-list.order-widget` as Bootstrap dropdown.

### 3. Default Grid Configuration

**Question**: What should the default grid layout be?

**Decision**: Single column across all screen sizes

**Rationale**: Single column is the safest default as it works for all content types and screen sizes. Developers can easily override via the `grid` attribute for multi-column responsive layouts.

**Implementation**: `grid = {}` defaults to `cols=1` in the grid component.

### 4. Mixin Architecture

**Question**: What is the mixin inheritance structure?

**Decision**:

- `SearchMixin` - Search functionality
- `OrderMixin` - Ordering functionality
- `SearchOrderMixin(SearchMixin, OrderMixin)` - Combined search + order
- `ListItemTemplateMixin` - List item template rendering
- `MVPListViewMixin(SearchOrderMixin, ListItemTemplateMixin)` - Full feature set

**Rationale**: Allows developers to use individual mixins independently or use the combined MVPListViewMixin for full functionality.

**Implementation**: Already implemented in `mvp/views.py`.

### 5. Attribute Override Pattern

**Question**: How should class-based attributes be overridable?

**Decision**: All attributes have corresponding `get_*()` methods following Django CBV patterns.

**Examples**:

- `search_fields` → `get_search_fields()`
- `order_by` → `get_order_by_choices()`
- `list_item_template` → `get_list_item_template()`
- `grid` → `get_grid_config()`
- `page_title` → `get_page_title()`

**Implementation**: Already implemented in `mvp/views.py`.

### 6. django-filter Integration

**Question**: How does search/ordering interact with django-filter?

**Decision**: Search and ordering work IN ADDITION TO django-filter filtering. They are complementary, not alternatives.

**Rationale**: Users may want to filter (e.g., category=Electronics), then search within those results, then sort by price.

**Implementation**: Each applies to the queryset in sequence via `get_queryset()` method chaining.

## Technology Decisions

### Template Tag for List Item Rendering

**Decision**: Use custom template tag `{% render_list_item object template %}`

**Implementation**: Already exists in `mvp/templatetags/mvp.py`

**Usage**: `{% render_list_item object list_item_template %}`

### Pagination Component

**Decision**: Use existing `c-page.footer.pagination` component

**Issue Found**: Currently uses DataTables context (`table.page.start_index`). Needs update to use standard Django pagination (`page_obj`).

### Filter Sidebar

**Decision**: Use existing `c-sidebar.filter` component with crispy-forms

**Implementation**: Renders `filter.form` using crispy-forms in a right-side sliding sidebar.

## Best Practices Applied

### Django Class-Based Views

- Mixins use cooperative inheritance (`super()` calls)
- Context data added via `get_context_data()` override
- Queryset modifications via `get_queryset()` override
- Template resolution via `get_template_names()` override

### Django Cotton Components

- Components use snake_case naming (e.g., `c-list.search-widget`)
- Responsive grid uses Bootstrap 5 grid classes
- Components follow slot-based composition pattern

### Testing Strategy

- Unit tests for mixin functionality (pytest)
- Integration tests for view rendering (pytest-django)
- E2E tests for user workflows (pytest-playwright)

## References

- Django CBV documentation: <https://docs.djangoproject.com/en/4.2/topics/class-based-views/>
- django-filter documentation: <https://django-filter.readthedocs.io/>
- django-cotton documentation: <https://django-cotton.com/>
- Bootstrap 5 grid: <https://getbootstrap.com/docs/5.3/layout/grid/>
