# Feature Specification: Dashboard List View Mixin

**Feature Branch**: `008-dash-list-view`
**Created**: February 4, 2026
**Status**: Draft
**Input**: User description: "This feature will cover the behavior of the MVPListViewMixin. This mixin class can be mixed into any list-based view (e.g. ListView, FilterView). The benefits of this mixin for developers is that they can provide a list item template which will automatically be used to populate the actual list of content. Everything else will be configurable via class-based variables. When they specify search_fields, we'll have a search bar show up in the page header. When they specify order_by fields, we'll have an order by toggle automatically show up in the page header. If they utilize something like FilterView by Django filters, then we'll have a filter toggle show up that will open a filters sidebar. Developers should be able to configure the actual grid by specifying a grid attribute on the class itself. This grid attribute will be passed directly to a Django Cotton component to configure how the grid appears."

## Clarifications

### Session 2026-02-04

- Q: What page elements are automatically displayed in a basic list view? → A: The page displays: (1) Model's verbose name as the page title at the top, (2) A grid (defaulting to single column) of objects rendered with the list_item_template, (3) If pagination is enabled, a footer showing pagination information and entry counts on the left, with pagination navigation links on the right.

- Q: What is the mixin architecture for MVPListViewMixin? → A: MVPListViewMixin is built on four foundational mixins: (1) SearchMixin provides search functionality, (2) OrderMixin provides ordering/sorting functionality, (3) SearchOrderMixin combines SearchMixin and OrderMixin, (4) ListItemTemplateMixin provides list item template rendering. MVPListViewMixin inherits from SearchOrderMixin and ListItemTemplateMixin. All mixins must function correctly for this feature.

- Q: Can the page title and other class-based attributes be overridden? → A: Yes. The page title defaults to the model's verbose name but can be overridden via a class-based attribute or a method. In fact, ALL class-based attributes must be overridable via methods.

- Q: How do search and ordering relate to django-filter filtering? → A: Search (from SearchMixin) and ordering (from OrderMixin) work in ADDITION to any filtering provided by django-filter. They are complementary, not alternatives. Users can filter, search, and sort simultaneously.

- Q: What search operator behavior should be used when users enter multiple words? → A: OR matching - any word matches (broader results). This provides better user experience by showing more results and reducing "no results" scenarios.

- Q: What UI widget type should be used for ordering controls in the page header? → A: Dropdown menu - compact, single selection. This is space-efficient (critical for headers with multiple widgets), familiar to users, and works well on mobile devices.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic List Display (Priority: P1)

A developer wants to create a simple list view of database records with minimal configuration. They add the MVPListViewMixin to their ListView, specify a list item template, and immediately see a complete page with: the model's verbose name as the page title, their data displayed in a single-column grid (by default), and if pagination is enabled, a footer showing entry counts and pagination controls.

**Why this priority**: This is the foundational functionality - without the ability to display a basic list, none of the other features matter. It provides immediate value by simplifying list view creation with automatic page structure.

**Independent Test**: Can be fully tested by creating a view class that mixes in MVPListViewMixin, specifying only a model and list_item_template, then verifying: (1) the page displays the model's verbose name as title, (2) objects render in a single-column grid using the template, (3) if pagination is configured, the footer displays correctly with entry counts and navigation links.

**Acceptance Scenarios**:

1. **Given** a developer has a model with data, **When** they create a view mixing MVPListViewMixin with only model and list_item_template specified, **Then** the page displays the model's verbose name as the title, all records in a default single-column grid using the specified template
2. **Given** a list view is displaying records, **When** a user accesses the page, **Then** each record is rendered using the developer-specified list item template within the grid
3. **Given** no grid configuration is specified, **When** the list renders, **Then** it uses a default single-column grid layout
4. **Given** pagination is enabled on the view, **When** the page renders, **Then** a footer appears showing pagination information and entry counts on the left side, with pagination navigation links on the right side
5. **Given** pagination is not enabled, **When** the page renders, **Then** no pagination footer is displayed

---

### User Story 2 - Custom Grid Configuration (Priority: P2)

A developer wants to control how list items are arranged visually. They set a grid attribute on their view class, and the system automatically passes this configuration to the underlying grid component to create the desired layout (e.g., 3 columns on desktop, 1 on mobile).

**Why this priority**: Visual presentation is important for user experience, but the feature is still functional without custom layouts. This adds polish and flexibility.

**Independent Test**: Can be tested by creating a view with a custom grid attribute and verifying that the rendered output reflects the specified grid configuration (column counts, spacing, responsive behavior).

**Acceptance Scenarios**:

1. **Given** a developer specifies a grid attribute on the view class, **When** the list renders, **Then** the grid layout matches the specified configuration
2. **Given** different grid configurations for different screen sizes, **When** users access the page on various devices, **Then** the appropriate layout is displayed for each screen size
3. **Given** invalid grid configuration, **When** the view is rendered, **Then** the system falls back to default grid layout without errors

---

### User Story 3 - Search Functionality (Priority: P2)

A developer adds search_fields to their view class. The system automatically displays a search bar in the page header. Users can type search terms and see the list filtered in real-time to show only matching records.

**Why this priority**: Search is critical for usability in lists with many items, but the feature works without it for smaller datasets.

**Independent Test**: Can be tested by adding search_fields to a view class, verifying a search bar appears, entering search terms, and confirming only matching records are displayed.

**Acceptance Scenarios**:

1. **Given** a developer specifies search_fields on the view class, **When** the page loads, **Then** a search bar appears in the page header
2. **Given** a search bar is visible, **When** a user enters search terms, **Then** the list updates to show only records matching the search criteria across specified fields
3. **Given** no search_fields are specified, **When** the page loads, **Then** no search bar is displayed
4. **Given** search terms with no matches, **When** a user searches, **Then** the list displays an appropriate "no results" message

---

### User Story 4 - Ordering Controls (Priority: P2)

A developer specifies order_by fields on their view class. The system automatically adds ordering controls to the page header. Users can click these controls to order the list by different fields in ascending or descending order.

**Why this priority**: Ordering improves data navigation but isn't essential for viewing data. It's commonly expected in list interfaces.

**Independent Test**: Can be tested by adding order_by fields to a view, verifying ordering controls appear, clicking them, and confirming the list reorders correctly.

**Acceptance Scenarios**:

1. **Given** a developer specifies order_by fields on the view class, **When** the page loads, **Then** ordering controls appear in the page header
2. **Given** ordering controls are visible, **When** a user selects a field to order by, **Then** the list reorders according to that field in ascending order
3. **Given** a field is already selected for ordering, **When** a user clicks the same control again, **Then** the order direction toggles between ascending and descending
4. **Given** no order_by fields are specified, **When** the page loads, **Then** no ordering controls are displayed
5. **Given** multiple ordering fields, **When** a user selects different fields, **Then** the list updates to reflect the newly selected ordering field

---

### User Story 5 - Filter Sidebar Integration (Priority: P3)

A developer uses a FilterView-based view (with django-filter) mixed with MVPListViewMixin. The system automatically detects the filters and displays a filter toggle button in the page header. When users click it, a sidebar opens with the available filters, allowing them to narrow down the list by various criteria.

**Why this priority**: Advanced filtering is valuable for power users but not essential for basic usage. Many views may not need complex filters.

**Independent Test**: Can be tested by creating a FilterView with MVPListViewMixin, verifying a filter toggle appears, clicking it to open the sidebar, applying filters, and confirming the list updates accordingly.

**Acceptance Scenarios**:

1. **Given** a developer uses FilterView with filters defined, **When** the page loads, **Then** a filter toggle button appears in the page header
2. **Given** a filter toggle button is visible, **When** a user clicks it, **Then** a sidebar opens displaying available filter controls
3. **Given** the filter sidebar is open, **When** a user applies filters, **Then** the list updates to show only records matching the filter criteria
4. **Given** the filter sidebar is open, **When** a user clicks the toggle again or a close button, **Then** the sidebar closes
5. **Given** a standard ListView without FilterView, **When** the page loads, **Then** no filter toggle is displayed
6. **Given** filters are applied, **When** a user clears all filters, **Then** the full list is displayed again

---

### Edge Cases

- What happens when search_fields references a non-existent model field?
- How does the system handle empty lists (no records to display)?
- What happens when grid configuration conflicts with the number of items?
- How does the page header accommodate multiple widgets (search bar, sort controls, filter toggle) on small screens?
- What happens when a user applies filters or search that result in zero matches?
- How does the system handle extremely long list item templates or complex grid configurations that impact performance?
- What happens when order_by fields reference non-sortable fields (e.g., many-to-many relationships)?
- How does pagination interact with search, sort, and filter functionality?

## Requirements *(mandatory)*

### Functional Requirements

#### Mixin Architecture (Critical Foundation)

- **FR-001**: System MUST provide a SearchMixin class that adds search functionality to any list-based view
- **FR-002**: System MUST provide an OrderMixin class that adds ordering/sorting functionality to any list-based view
- **FR-003**: System MUST provide a SearchOrderMixin class that inherits from both SearchMixin and OrderMixin, combining search and ordering functionality
- **FR-004**: System MUST provide a ListItemTemplateMixin class that handles rendering list items using a specified template
- **FR-005**: System MUST provide an MVPListViewMixin class that inherits from SearchOrderMixin and ListItemTemplateMixin
- **FR-006**: System MUST ensure all mixins (SearchMixin, OrderMixin, SearchOrderMixin, ListItemTemplateMixin, MVPListViewMixin) function correctly both independently and when combined
- **FR-007**: System MUST allow MVPListViewMixin to be mixed into any Django list-based view class (ListView, FilterView, etc.)

#### Page Structure & Display

- **FR-008**: System MUST automatically display the model's verbose name as the page title by default
- **FR-009**: System MUST allow the page title to be overridden via a class-based attribute or method
- **FR-010**: System MUST allow ALL class-based attributes across all mixins to be overridable via corresponding methods (e.g., get_page_title(), get_grid(), get_search_fields())
- **FR-011**: System MUST allow developers to specify a list_item_template attribute that defines how each record is rendered
- **FR-012**: System MUST automatically render each object in the queryset using the specified list_item_template within a grid layout
- **FR-013**: System MUST default to a single-column grid layout when no grid attribute is specified
- **FR-014**: System MUST provide a grid attribute that developers can set to configure grid layout
- **FR-015**: System MUST pass the grid attribute value to the underlying Cotton grid component for rendering
- **FR-016**: System MUST automatically display a pagination footer when pagination is enabled on the view
- **FR-017**: System MUST display pagination information and entry counts on the left side of the pagination footer
- **FR-018**: System MUST display pagination navigation links on the right side of the pagination footer

#### Search Functionality (SearchMixin)

- **FR-019**: System MUST automatically display a search bar in the page header when search_fields is specified on the view class
- **FR-020**: System MUST filter the queryset based on user search input across all fields specified in search_fields using OR matching (any word matches) for multi-word searches (split by any whitespace: space, tab, newline)
- **FR-021**: System MUST apply search filtering in ADDITION to any django-filter filtering (search does not replace filtering)

#### Ordering Functionality (OrderMixin)

- **FR-022**: System MUST automatically display ordering controls as a dropdown menu in the page header when order_by fields are specified on the view class (dropdown label shows current ordering selection)
- **FR-023**: System MUST reorder the queryset when users select a sort field from the dropdown
- **FR-024**: System MUST support toggling between ascending and descending sort order
- **FR-025**: System MUST apply ordering in ADDITION to any django-filter filtering (ordering does not replace filtering)

#### Filter Integration (django-filter)

- **FR-026**: System MUST automatically detect when a view is using FilterView (django-filter) and display a filter toggle button
- **FR-027**: System MUST display a filter sidebar when the filter toggle is activated
- **FR-028**: System MUST populate the filter sidebar with filter controls defined by django-filter
- **FR-029**: System MUST update the displayed list when filters are applied or removed
- **FR-030**: System MUST support simultaneous use of django-filter filtering, search functionality, and ordering functionality

#### General Requirements

- **FR-031**: System MUST handle empty querysets gracefully by displaying an appropriate message
- **FR-032**: System MUST support responsive grid layouts that adapt to different screen sizes
- **FR-033**: System MUST integrate with the existing MVP page header structure for displaying controls
- **FR-034**: System MUST preserve user-selected sort, search, and filter state when paginating through results

### Key Entities *(include if feature involves data)*

- **SearchMixin**: Mixin providing search functionality
  - Attributes: search_fields (list of model fields to search across)
  - Methods: get_search_fields(), apply_search() (or similar)
  - Behavior: Adds search bar to page header, filters queryset based on search input

- **OrderMixin**: Mixin providing ordering/sorting functionality
  - Attributes: order_by fields (list of sortable fields)
  - Methods: get_order_fields(), apply_ordering() (or similar)
  - Behavior: Adds sort controls to page header, reorders queryset

- **SearchOrderMixin**: Combined mixin inheriting from SearchMixin and OrderMixin
  - Inherits all attributes and methods from both parent mixins
  - Behavior: Provides both search and ordering functionality together

- **ListItemTemplateMixin**: Mixin providing list item template rendering
  - Attributes: list_item_template (path to template file), grid (grid configuration)
  - Methods: get_list_item_template(), get_grid() (or similar)
  - Behavior: Renders each queryset object using the specified template within a grid layout

- **MVPListViewMixin**: Top-level mixin inheriting from SearchOrderMixin and ListItemTemplateMixin
  - Inherits all functionality from SearchMixin, OrderMixin, and ListItemTemplateMixin
  - Additional attributes: page_title (or uses model verbose_name)
  - Methods: get_page_title() and all inherited methods
  - Relationships: Can be mixed into Django ListView, FilterView, or other list-based views

- **List Item Template**: A template file that defines how a single record should be rendered
  - Contains: HTML structure and display logic for one list item
  - Receives: Individual queryset object as context

- **Grid Configuration**: Configuration data specifying layout properties
  - Properties: Column counts, spacing, responsive breakpoints
  - Format: Compatible with Django Cotton grid component

- **Page Header Widgets**: UI controls displayed in the dashboard page header
  - Types: Search bar (text input), sort dropdown menu (single selection), filter toggle button
  - Behavior: Conditionally appear based on view configuration and mixin presence
  - Design: Space-efficient to accommodate multiple widgets on small screens

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can create a fully functional list view by adding MVPListViewMixin and specifying only model and list_item_template (under 10 lines of code)
- **SC-002**: Search functionality returns filtered results in under 500ms for lists with up to 10,000 records (measured on typical development hardware with PostgreSQL/SQLite, single process)
- **SC-003**: New users can find and apply all available list operations (search, ordering, filter) within 2 minutes without external documentation by using visible UI controls
- **SC-004**: Grid layouts correctly adapt to screen sizes from mobile (320px) to desktop (1920px+) without horizontal scrolling
- **SC-005**: List views with all features enabled (search, sort, filter) render initial page in under 2 seconds
- **SC-006**: Developers can implement list views 60% faster: 10 lines with mixin vs 50+ lines manual (baseline: manual ListView with search, ordering, pagination requires ~50 lines including view class, URL, template modifications)
- **SC-007**: All page header widgets (search, sort, filter) remain accessible and functional on screens as small as 375px width
- **SC-008**: Sort, search, and filter states persist correctly through pagination with zero data loss

## Assumptions

- Django Cotton components for grid layout are already available and documented
- The mixin architecture (SearchMixin, OrderMixin, SearchOrderMixin, ListItemTemplateMixin) follows Django's standard mixin patterns
- Each mixin can be used independently or in combination with others
- The MVPListViewMixin will integrate with the existing MVP dashboard layout structure
- Developers using these mixins are familiar with basic Django class-based views
- The django-filter library is an optional dependency for filter functionality
- Search, ordering, and filtering (django-filter) are complementary and work together simultaneously
- Default grid configuration is a single column across all screen sizes; developers can override via the grid attribute for responsive multi-column layouts
- All class-based attributes follow the Django CBV pattern of having corresponding get_* methods for dynamic override
- Model verbose_name (or verbose_name_plural) is used as the page title automatically
- Search will use case-insensitive matching by default
- Multi-word searches use OR matching (any word matches), providing broader results and better user experience
- Pagination will be handled by standard Django pagination and is configured separately via paginate_by or get_paginate_by()
- Pagination footer layout: left side shows entry information ("Showing X to Y of Z entries"), right side shows navigation links
- List item templates receive the object as 'object' in the template context
- Page header is implemented using blocks that can be extended
- Filter sidebar will slide in from the right side of the screen
- Search and filter operations will trigger server-side requests (not client-side filtering)
- The system assumes reasonable list sizes; extremely large datasets may require additional optimization

## Dependencies

- Django Cotton for grid components
- Django core ListView and pagination functionality
- django-filter library (optional, for filter functionality)
- Bootstrap or similar CSS framework for responsive design
- Existing MVP dashboard layout and page header blocks
- HTMX or similar library for dynamic search/sort/filter updates (if implementing without full page reloads)

## Out of Scope

- Client-side (JavaScript-based) filtering or searching
- Advanced filter UI customization beyond django-filter defaults
- Export functionality (CSV, Excel, PDF)
- Bulk actions on list items (select multiple, delete, etc.)
- Inline editing of list items
- Drag-and-drop reordering
- List view state persistence across sessions
- Advanced search features (fuzzy matching, autocomplete)
- Custom sort algorithms beyond database ordering
- Performance optimization for lists with >100,000 records
- Nested or hierarchical list displays
- Virtualized scrolling for performance
- Real-time updates or live data refresh
