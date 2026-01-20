# Feature Specification: Inner Layout System

**Feature Branch**: `006-page-layout`
**Created**: January 16, 2026
**Status**: Draft
**Input**: User description: "This feature introduces an inner layout system built using Django Cotton components..."

## Clarifications

### Session 2026-01-16

- Q: The specification mentions that toolbar and footer should have "sticky positioning" (FR-012), but doesn't specify whether they should be sticky within the scrolling area or fixed to the viewport edges. This impacts the CSS implementation and user experience significantly. → A: Sticky within scrolling area (CSS position: sticky) - toolbar sticks to top when scrolling down, footer to bottom when scrolling up
- Q: The specification describes a "secondary sidebar" on the right side, but doesn't clarify whether this sidebar should be collapsible/toggleable by the end user or only configurable by developers via settings. This affects the UI implementation and user interaction patterns. → A: Both - configurable default state plus optional user toggle functionality (aligns with outer layout sidebar behavior)
- Q: The specification mentions responsive behavior for the secondary sidebar (FR-014) - it should "collapse or hide" on smaller screens. However, it doesn't specify which breakpoint(s) should trigger this behavior or whether it should collapse vs hide. → A: Hide below Bootstrap's 'lg' breakpoint (1024px) by default, but breakpoint is configurable by developers
- Q: The specification requires the main inner content area to "automatically fill available space" (FR-006) after accounting for toolbar, footer, and sidebar. However, it doesn't specify how the layout should be structured - whether using CSS Grid, Flexbox, or another approach. → A: CSS Grid layout - following AdminLTE 4's outer app-wrapper pattern with grid template for fixed/flexible areas
- Q: The specification mentions that the inner layout configuration should integrate with the existing MVP configuration dictionary (FR-007), but doesn't specify the configuration structure. → A: Inner layout is NOT configurable via MVP settings dict - configuration is template-driven through Cotton component attributes

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Inner Layout Usage (Priority: P1)

A developer needs to create a full-screen data table page with a persistent toolbar at the top and footer at the bottom. They want the table content to fill all available space between these fixed elements, creating a clean, focused interface for data viewing and manipulation.

**Why this priority**: This is the core use case driving the feature request - providing structured full-screen layouts for data-intensive applications.

**Independent Test**: Can be fully tested by creating a page that uses the inner layout with toolbar and main content area, verifying the content fills available space and toolbar remains visible during scrolling.

**Acceptance Scenarios**:

1. **Given** a developer creates a page extending the base layout, **When** they add the inner layout component with a toolbar and content area, **Then** the toolbar appears at the top of the main content area with the content filling remaining space
2. **Given** an inner layout with long scrolling content, **When** the user scrolls down, **Then** the toolbar sticks to the top of the scrolling container while content scrolls beneath it
3. **Given** a developer needs a footer, **When** they include the inner layout footer component, **Then** the footer sticks to the bottom of the scrolling container when scrolling

---

### User Story 2 - Secondary Sidebar Integration (Priority: P2)

A developer building a mapping application needs to display the map in the main content area with a properties panel or legend on the right side. The secondary sidebar should be configurable to show/hide and adjust its width based on the application's needs.

**Why this priority**: Adds significant value for applications requiring multi-panel layouts, but the core inner layout is functional without it.

**Independent Test**: Can be tested by creating a page with inner layout including both main content and right sidebar, verifying the sidebar displays correctly and content area adjusts accordingly.

**Acceptance Scenarios**:

1. **Given** a developer adds a secondary sidebar to the inner layout, **When** the page renders, **Then** the sidebar appears on the right side with the main content area adjusted to accommodate it
2. **Given** a secondary sidebar is configured with specific width, **When** the page renders, **Then** the sidebar displays at the specified width
3. **Given** a secondary sidebar is set to hidden via configuration, **When** the page renders, **Then** the sidebar does not appear and content area uses full width
4. **Given** a secondary sidebar with user toggle enabled, **When** the user clicks the toggle button, **Then** the sidebar collapses/expands and content area adjusts accordingly

---

### User Story 3 - Template-Driven Configuration (Priority: P2)

A developer wants to configure inner layout behavior (toolbar visibility, footer visibility, sidebar width) through template attributes and component properties rather than global settings. This allows each page to have its own layout configuration while maintaining consistent defaults and patterns.

**Why this priority**: Configuration validation and defaults are important for robustness, but basic layout functionality (US1) can work with implicit defaults. This is polish that enhances developer experience but isn't required for MVP.

**Independent Test**: Can be tested by creating multiple pages with different inner layout configurations through component attributes, verifying each page displays independently.

**Acceptance Scenarios**:

1. **Given** a developer sets toolbar visibility to false via component attribute, **When** the page renders, **Then** no toolbar appears
2. **Given** a developer configures sidebar width via component attribute, **When** the page renders, **Then** the sidebar displays at the specified width
3. **Given** multiple component configuration attributes are set, **When** the page renders, **Then** all configuration options are applied correctly

---

### Edge Cases

- What happens when both outer sidebar and inner sidebar are visible? (Should work together without conflict - outer sidebar on left, inner sidebar on right)
- How does the inner layout handle very narrow viewport widths? (Should maintain responsive behavior, potentially stacking or hiding elements based on breakpoints)
- What happens if developer nests inner layouts within inner layouts? (Not recommended but should fail gracefully or document as unsupported)
- How does the toolbar handle overflow content when there are many toolbar items? (Should provide scrolling or wrapping behavior)
- What happens when footer content is very tall? (Should maintain fixed footer position with appropriate height handling)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a Cotton component for inner layout that can be used within the main content area of the outer layout
- **FR-002**: Inner layout MUST include four configurable areas: toolbar (top), footer (bottom), secondary sidebar (right), and main content area (center)
- **FR-003**: Toolbar MUST support configuration options for visibility (via slot presence) and styling classes (via `class` attribute)
- **FR-004**: Footer MUST support configuration options for visibility (via slot presence) and styling classes (via `class` attribute)
- **FR-005**: Secondary sidebar MUST support configuration options for visibility, width, and positioning (right side), with optional user toggle button to show/hide sidebar during runtime
- **FR-006**: Main inner content area MUST automatically fill available space after accounting for toolbar, footer, and sidebar, using CSS Grid layout structure (following AdminLTE 4 outer layout pattern)
- **FR-007**: Inner layout configuration MUST be template-driven through Cotton component attributes (toolbar_visible, footer_visible, sidebar_width, etc.)
- **FR-008**: System MUST support optional usage - developers can choose not to use inner layout and have complete freedom in main content area
- **FR-009**: Inner layout MUST NOT conflict with or break existing outer layout functionality (header, outer sidebar, footer, main content area)
- **FR-010**: Inner layout MUST use Django Cotton's slot system for flexible content composition
- **FR-011**: Toolbar and footer MUST use CSS position: sticky - toolbar sticks to top of scrolling area when scrolling down, footer sticks to bottom when scrolling up (not fixed to viewport)
- **FR-012**: System MUST provide sensible default values for all component attributes when not explicitly set
- **FR-013**: Secondary sidebar MUST hide (not just narrow) on smaller screen sizes, defaulting to Bootstrap's 'lg' breakpoint (1024px), with the breakpoint configurable via component attribute
- **FR-014**: When sidebar includes user toggle functionality, the toggle state SHOULD persist during the user session (e.g., via sessionStorage or similar)

### Key Entities

- **Inner Layout Component**: Cotton component that renders the nested layout structure within the outer layout's main content area using CSS Grid (mirroring AdminLTE 4's outer app-wrapper pattern), configured via component attributes
- **Toolbar Area**: Top section of inner layout for action buttons, filters, breadcrumbs, or page-specific controls
- **Footer Area**: Bottom section of inner layout for pagination, summary information, or action buttons
- **Secondary Sidebar**: Right-side panel for supplementary content, properties, filters, or navigation
- **Main Inner Content**: Central content area that fills available space and contains primary page content

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can implement a full-screen layout with fixed toolbar and footer in under 5 minutes using the inner layout component
- **SC-002**: Inner layout component attributes provide consistent configuration interface across all pages using inner layout
- **SC-003**: Pages using inner layout render correctly across viewport widths from 320px (mobile) to 4K displays (3840px+)
- **SC-004**: Inner layout components maintain visual consistency with AdminLTE 4 design system and outer layout styling
- **SC-005**: Main inner content area automatically adjusts dimensions when toolbar, footer, or sidebar visibility changes, requiring no manual layout calculations
- **SC-006**: Documentation enables developers unfamiliar with the codebase to implement inner layout in under 10 minutes
