# Feature Specification: Inner Layout Component

**Feature Branch**: `002-inner-layout`  
**Created**: December 23, 2025  
**Status**: Draft  
**Input**: User description: "Inner layout is a django-cotton component that is typically used by end-users direct in template. Basic customization can be provided via data attributes on the component itself. The component provides a primary_sidebar and a secondary_sidebar slot which are both optional. The slots are empty (only provide the correct location for usage). Users are advised to make use of a pre-built sidebar component (typically located in cotton/sidebar/*). The only current component is the default provided by index.html. Users can configure the sidebar direct on the sidebar component itself. By not providing a sidebar (e.g. not declaring the slot inside the inner layout component), the sidebar will be empty and the main content layout will expand to fill space. Do not include sidebars themselves in this specification. We will provide a separate specification on building and using sidebars."

## Clarifications

### Session 2025-12-23

- Q: How should the component handle declared-but-empty sidebar slots? → A: Do not reserve space for empty slots (collapse/hide empty columns)
- Q: What should be the canonical terminology for the sidebar slots? → A: Use slot names (primary_sidebar/secondary_sidebar) as canonical terms, mention position descriptively
- Q: What should be the default width for sidebar slots? → A: 280px for primary_sidebar, 250px for secondary_sidebar
- Q: At what responsive breakpoint should sidebars hide or collapse on smaller viewports? → A: "Offcanvas mode" means sidebars switch from fixed in-flow layout to Bootstrap offcanvas panels (can be toggled to slide in). "Collapse mode" means sidebar width reduces to fit-content (usually icons only). Default offcanvas breakpoint is "md" (768px). Constraint: A sidebar MAY NOT collapse when in offcanvas mode.
- Q: How should users provide the main content to the inner layout component? → A: Use default unnamed slot (wrap content directly in component tags)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Content Layout Without Sidebars (Priority: P1)

A developer building a simple page wants to display main content without any sidebars. They use the inner layout component in their template, wrapping their content directly in the component tags (using the default slot). The layout automatically expands the content area to fill the available space.

**Why this priority**: This is the most fundamental use case - displaying content. If this doesn't work, the component has no value. It represents the MVP for the inner layout system.

**Independent Test**: Can be fully tested by including the inner layout component in a template with only main content (no named slots declared) and verifying that the content renders and fills the available width without sidebars. Delivers immediate value by providing a working content area.

**Acceptance Scenarios**:

1. **Given** a developer includes the inner layout component in their template, **When** they provide only main content in the default slot (no sidebar slots declared), **Then** the content renders in a single column layout filling the available width
2. **Given** the inner layout component is rendering without sidebars, **When** the viewport is resized, **Then** the main content area expands/contracts to utilize the full available width responsively

---

### User Story 2 - Single Sidebar Layout (Priority: P2)

A developer building a documentation page wants a primary_sidebar for navigation and main content area. They include the inner layout component and populate the primary_sidebar slot with a pre-built sidebar component from cotton/sidebar/*. The layout positions the sidebar (on the left) and content appropriately.

**Why this priority**: Single sidebar layouts are extremely common for documentation, blogs, and many web applications. This represents the second most common use case.

**Independent Test**: Can be tested by declaring the primary_sidebar slot with sidebar content and verifying the two-column layout renders correctly with proper spacing and responsive behavior. Delivers a functional sidebar layout pattern.

**Acceptance Scenarios**:

1. **Given** a developer includes the inner layout component, **When** they declare the primary_sidebar slot with a sidebar component, **Then** the layout renders with the primary_sidebar (positioned on the left) and main content area side-by-side
2. **Given** a single sidebar layout is active, **When** the viewport shrinks below the md breakpoint (768px), **Then** the sidebar switches to offcanvas mode (Bootstrap offcanvas panel that can be toggled to slide in from off-page) and main content expands to full width
3. **Given** the primary_sidebar slot is not declared in the template, **When** the layout renders, **Then** the sidebar is not rendered and main content expands to fill the available width

---

### User Story 3 - Dual Sidebar Layout (Priority: P3)

A developer building a complex dashboard wants both primary_sidebar and secondary_sidebar with main content in the center. They include the inner layout component and populate both primary_sidebar and secondary_sidebar slots. The layout creates a three-column layout with proper spacing.

**Why this priority**: Dual sidebar layouts are less common but important for complex interfaces like admin panels, dashboards, and documentation with supplementary content. This is an advanced use case.

**Independent Test**: Can be tested by declaring both sidebar slots with content and verifying the three-column layout renders with proper proportions and spacing. Delivers an advanced layout pattern for complex interfaces.

**Acceptance Scenarios**:

1. **Given** a developer includes the inner layout component, **When** they declare both primary_sidebar and secondary_sidebar slots, **Then** the layout renders with primary_sidebar (positioned on the left), main content, and secondary_sidebar (positioned on the right) in a three-column layout
2. **Given** a dual sidebar layout is active, **When** the viewport shrinks below the md breakpoint, **Then** both sidebars switch to offcanvas mode (both convert to Bootstrap offcanvas panels accessible via toggle buttons)
3. **Given** only one sidebar slot is declared in the template, **When** the layout renders, **Then** the layout renders as a single-sidebar layout (undeclared sidebar is not rendered and does not reserve space)

---

### User Story 4 - Custom Layout Configuration via Component Parameters (Priority: P3)

A developer wants to customize the inner layout behavior (e.g., sidebar widths, responsive breakpoints, spacing) without modifying the component itself. They use component parameters on the inner layout component tag to specify configuration values. The layout applies these customizations.

**Why this priority**: This provides flexibility and customization without requiring component modifications. It's important for advanced users but not critical for basic functionality.

**Independent Test**: Can be tested by adding data attributes to the component tag and verifying the layout renders with the specified customizations (e.g., custom sidebar width). Delivers configuration flexibility.

**Acceptance Scenarios**:

1. **Given** a developer includes the inner layout component with custom parameters, **When** they specify custom sidebar widths (e.g., primary_width="320px"), **Then** the layout renders with the specified sidebar width instead of the default (280px for primary_sidebar, 250px for secondary_sidebar)
2. **Given** the inner layout component has configuration parameters, **When** they specify responsive breakpoints (e.g., breakpoint="lg"), **Then** the layout uses those breakpoints for responsive behavior
3. **Given** custom spacing is specified via component parameters (e.g., gap="3"), **Then** the spacing between columns matches the specified value

---

### Edge Cases

- What happens when a sidebar slot is not declared in the template? (Sidebar is not rendered and main content expands to fill space)
- What happens when main content is extremely wide or contains non-wrapping content? (Layout handles overflow with scrolling within regions)
- What happens when both sidebars are declared on very small viewports? (Both sidebars switch to offcanvas mode accessible via toggle buttons)
- What happens when invalid component parameter values are provided? (Layout falls back to default values: 280px primary, 250px secondary, md breakpoint)
- What happens when the inner layout is nested inside another inner layout? (Nesting is not supported; behavior is undefined)
- What happens when a sidebar is configured to both collapse and hide at the same breakpoint? (Hide/offcanvas mode takes precedence; sidebar cannot be collapsed while in offcanvas mode)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an inner layout component that can be included directly in Django templates
- **FR-002**: Component MUST support a default (unnamed) slot for main content that is always rendered
- **FR-003**: Component MUST provide an optional primary_sidebar slot that renders on the left side of the main content
- **FR-004**: Component MUST provide an optional secondary_sidebar slot that renders on the right side of the main content
- **FR-005**: Component MUST automatically expand main content to fill available width when no sidebars are declared
- **FR-006**: Component MUST support customization via component parameters (rendered as data attributes and CSS variables in HTML)
- **FR-007**: Component MUST be responsive and adapt layout based on viewport size with two modes: offcanvas mode (switch to Bootstrap offcanvas panel) and collapse mode (reduce width to fit-content)
- **FR-008**: Component MUST enforce that sidebars in offcanvas mode CANNOT also be in collapsed mode (offcanvas takes precedence)
- **FR-009**: Component MUST integrate with pre-built sidebar components from cotton/sidebar/* directory
- **FR-010**: Component MUST NOT render sidebar containers when sidebar slots are undeclared (undeclared slots do not render and do not reserve layout space)
- **FR-011**: Component MUST maintain consistent spacing and alignment across different layout configurations (no sidebars, one sidebar, two sidebars)
- **FR-012**: Component MUST be accessible and follow ARIA best practices for layout regions
- **FR-013**: Component MUST work within the outer layout system (inside .content-main or similar containers)
- **FR-014**: Component MUST apply semantic CSS class names following the naming conventions in STRUCTURE_AND_NAMING.md
- **FR-015**: Component MUST handle content overflow gracefully (scrolling within regions as needed)

### Key Entities

- **Inner Layout Component**: A Django-Cotton reusable component that provides a flexible multi-column layout structure. Contains slots for main content, primary_sidebar (positioned on the left), and secondary_sidebar (positioned on the right). Configured via data attributes.
- **Sidebar Slot**: Optional named slot within the inner layout component. Provides spatial positioning for sidebar content but does not dictate sidebar behavior or styling. Can be populated with pre-built sidebar components. The two sidebar slots are primary_sidebar and secondary_sidebar.
- **Main Content Area**: The default (unnamed) slot in the inner layout component. Always rendered. Expands to fill available width when sidebars are not present. Contains the primary page content. Users wrap content directly in component tags without needing to declare a named slot.
- **Layout Configuration**: Component parameters applied to the inner layout component tag that control layout behavior such as sidebar widths, responsive breakpoints, and spacing values. Parameters are rendered as HTML data attributes and CSS variables.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The inner layout component works with zero configuration (renders single-column layout without sidebar slots declared)
- **SC-002**: The inner layout component renders correctly across all major browsers (Chrome, Firefox, Safari, Edge) and viewport sizes (mobile, tablet, desktop)
- **SC-003**: Layouts remain stable and properly aligned when content changes dynamically (e.g., via HTMX updates)
- **SC-004**: Zero accessibility violations reported by automated testing tools (WAVE, axe) for the inner layout structure
- **SC-005**: Component parameters successfully override default values (widths, breakpoint, gap, collapse settings)
- **SC-006**: Responsive mode transitions occur automatically at configured breakpoints

## Assumptions

- Developers are already familiar with Django-Cotton component syntax and slot usage
- The outer layout system (from feature 001) is already implemented and provides the container in which inner layouts operate
- Pre-built sidebar components will be documented and available in cotton/sidebar/* (sidebar specification is separate)
- Bootstrap 5 is available for offcanvas behavior and optional utility classes (core layout uses framework-independent .content-* classes)
- Developers have access to STRUCTURE_AND_NAMING.md documentation for CSS class naming conventions
- The component will be used primarily for content-heavy pages (documentation, blogs, dashboards) rather than marketing/landing pages
- Default sidebar widths are 280px for primary_sidebar and 250px for secondary_sidebar, aligning with Bootstrap 5 standards and providing appropriate space for navigation (primary) versus supplementary content (secondary)
- Default responsive behavior: sidebars switch to offcanvas mode below the md breakpoint (768px)
- Sidebars can optionally collapse (reduce to fit-content width for icons) at configurable breakpoints, but not when in offcanvas mode
- Developers prefer configuration via component parameters over creating component variants

## Out of Scope

- **Sidebar Component Implementation**: The specification explicitly excludes sidebar components themselves (navigation, filters, widgets, etc.). These will be covered in a separate specification.
- **Content-Area Specific Components**: Components for cards, lists, forms, and other content patterns are not part of this specification.
- **Advanced Grid Layouts**: Complex grid patterns beyond the three-column sidebar layout (e.g., masonry, dashboard tiles) are not covered.
- **Animation/Transitions**: Animated transitions between layout states (e.g., sidebar slide-ins) are not part of the core layout component.
- **Layout Presets**: Pre-configured layout templates for specific use cases (blog layout, docs layout, etc.) are out of scope for this iteration.
- **Nested Inner Layouts**: Support for nesting inner layout components inside each other is not required.
