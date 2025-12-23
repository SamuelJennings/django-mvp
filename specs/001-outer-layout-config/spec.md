# Feature Specification: Outer Layout Configuration System

**Feature Branch**: `[001-outer-layout-config]`  
**Created**: 2025-12-23  
**Status**: ✅ Implemented (Ready for Merge)  
**Completed**: 2025-12-23  
**Input**: User description: "Build configuration object and outer layout system. You may examine tests/settings.py for an example config object and layouts/standard.html as an example of how to integrate the config object into the layout. This is done by passing config partials as dynamic django-cotton attrs."

## Clarifications

### Session 2025-12-23

 - Q: Where should responsive/toggle settings live in the configuration? → A: Per-region only (`sidebar.show_at`, `sidebar.collapsible`, `navbar.menu_visible_at`). No top-level `navigation.*`.
 - Q: What should the default layout configuration be out of the box? → A: Navbar-only by default with `sidebar.show_at=False`, `sidebar.collapsible=True`, `navbar.menu_visible_at="sm"`.
 - Q: Where should global actions render by default? → A: In the active navigation region (sidebar when in-flow; navbar otherwise) to avoid duplication.
 - Q: What is the brand image fallback behavior? → A: Use text fallback only when brand images are missing.

 

### User Story 1 - Configure navigation placement via per-region settings (Priority: P1)

 - Actions are never rendered in both regions simultaneously.

**Acceptance Scenarios**:

1. Given `sidebar.show_at=False` and `navbar.menu_visible_at="lg"`, When rendering a page, Then primary navigation appears in the navbar from the configured breakpoint and the sidebar remains offcanvas.
2. Given `sidebar.show_at="lg"` and any `navbar.menu_visible_at`, When viewport ≥ lg, Then primary navigation appears in the sidebar and the navbar shows utility items only (no duplicate primary nav).
3. Given `sidebar.show_at="lg"`, When viewport < lg, Then primary navigation is accessible via sidebar offcanvas; the navbar does not show the primary menu.

---

### User Story 2 - Brand and actions via configuration (Priority: P2)

An implementer sets brand text/images/icons and global actions (e.g., GitHub link) in configuration. The layout displays these consistently in the chosen regions.

**Why this priority**: Branding and quick actions are essential affordances for MVPs without editing templates.

**Independent Test**: Update brand image/text and actions list in configuration; verify brand appears in navbar/sidebar brand area and actions render in the configured area.

**Acceptance Scenarios**:

1. Given brand images for light/dark, When the page renders, Then the correct image is surfaced according to theme and the brand link text is visible.
2. Given actions=[{icon,text,href}], When the page renders, Then actions appear in their configured location with correct links and accessible labels.

---

### User Story 3 - Responsive behavior and toggles (Priority: P3)

An implementer configures sidebar toggle/collapsible and breakpoint behavior. The layout applies responsive classes and component attrs accordingly and remains usable with or without JavaScript.

**Why this priority**: Good responsiveness and progressive enhancement are non-negotiable for production quality.

**Independent Test**: Change `sidebar.show_at`, `sidebar.collapsible`, and `navbar.menu_visible_at` in configuration; verify class changes and behavior across mobile/tablet/desktop breakpoints. With JS disabled, navigation remains usable.

**Acceptance Scenarios**:

1. Given `sidebar.show_at="lg"`, When viewport is < lg, Then sidebar is hidden/accessible via navbar affordance; When ≥ lg, Then sidebar is visible without duplicating nav.
2. Given `sidebar.collapsible=True`, When user collapses sidebar, Then focus order and aria attributes remain valid and main content is accessible.

### Edge Cases

- Missing optional keys (e.g., no `actions`): layout renders with sensible defaults and no stray attributes.
- Invalid breakpoint value: system falls back to a safe default and logs a clear warning.
- `navbar.menu_visible_at` is ignored whenever `sidebar.show_at` is a breakpoint (sidebar in‑flow).
- Empty menu tree: navigation wrappers render safely without errors; no empty blocks displayed.
- Excessively long brand text: text truncates gracefully with accessible full text.
 - Missing brand images: fall back to brand text only; ensure accessible name and link remain correct.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST expose a single configuration object available to templates (e.g., via context processor) with top‑level keys: `brand`, `navbar`, `sidebar`, `actions`.
- **FR-002**: Navigation placement MUST be derived from per‑region settings with these rules:
	- If `sidebar.show_at` is `False`/`None`, the site is in navbar‑only mode; the navbar MAY show primary menu from `navbar.menu_visible_at` breakpoint.
	- If `sidebar.show_at` ∈ {`sm`,`md`,`lg`,`xl`,`xxl`}, primary navigation appears in the sidebar at all viewports; the navbar MUST NOT show primary menu.
- **FR-003**: `brand` MUST support text and distinct light/dark images and icons; templates MUST consume these via dynamic attrs without leaking internal variable names into HTML. If the appropriate theme image is missing, the system MUST fall back to brand text (accessible name preserved).
- **FR-004**: Responsive behavior MUST be configured per-region via `sidebar.show_at`, `sidebar.collapsible`, and `navbar.menu_visible_at`; no top-level `navigation` section is used.
- **FR-005**: `navbar` and `sidebar` MUST accept dicts passed into components via `:attrs="..."`, allowing component libraries to consume their options.
- **FR-006**: `actions` MUST be a list of action dicts ({icon,text,href,target?}) rendered without duplication in the active navigation region: if the sidebar is in-flow (`sidebar.show_at` is a breakpoint), actions render in the sidebar; otherwise, actions render in the navbar.
- **FR-007**: The outer layout template MUST integrate configuration strictly via dynamic attrs (Cotton), avoiding manual per-template duplication of config values.
- **FR-008**: The layout MUST remain functional without any CSS framework present and SHOULD be namespaced to avoid style collisions.
- **FR-009**: The system MUST enforce "single-source navigation rendering" based on navigation mode derived from `sidebar.show_at` (no navbar+sidebar duplicates of primary nav).
- **FR-010**: Defaults MUST be provided so a fresh install renders a usable layout without user configuration. Default values: navbar-only with `sidebar.show_at=False`, `sidebar.collapsible=True`, `navbar.menu_visible_at="sm"`.
- **FR-013**: The system MUST log clear warnings for invalid configuration values (e.g., invalid breakpoints, conflicting settings) with actionable remediation guidance.
- **FR-011**: Documentation MUST include a reference schema for configuration and examples for each layout mode.
- **FR-012**: Tests MUST cover: layout mode routing of navigation, brand/action rendering, responsive breakpoints, and absence of duplicate nav.

### Key Entities *(include if feature involves data)*

- **PageConfig**: A hierarchical configuration exposed to templates (keys: `brand`, `navbar`, `sidebar`, `actions`).
- **Brand**: Text and images/icons for light/dark themes.
- **Region Options** (`navbar`, `sidebar`): Dicts whose keys map to component attrs via Cotton.
- **Action**: UI action with `icon`, `text`, `href`, optional `target`.

### Terminology

- **Offcanvas**: Bootstrap's term for a collapsible sidebar overlay that slides in from the edge. Used interchangeably with "sidebar toggle" or "mobile sidebar" in this spec.
- **In-flow**: Sidebar is visible and occupies layout space (not offcanvas). Occurs when viewport ≥ `sidebar.show_at` breakpoint.
- **Active region**: The navigation region where primary menu and actions render (either sidebar or navbar, never both).
- **Navigation mode**: Layout behavior derived from `sidebar.show_at` value (navbar-only when False, sidebar mode when breakpoint).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Changing `sidebar.show_at`/`navbar.menu_visible_at` results in correct region rendering with zero duplicated primary navigation across modes.
- **SC-002**: A new installation renders a usable layout in under 1 minute of configuration (defaults only).
- **SC-003**: Layout renders correctly without any CSS framework present and remains responsive at mobile/tablet/desktop breakpoints.
- **SC-004**: Brand and actions render from configuration with 100% of specified items visible and keyboard accessible.
- **SC-005**: Test suite includes coverage for navigation placement, brand/actions, responsiveness; all pass on CI.
