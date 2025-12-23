# Research: Outer Layout Configuration System

Date: 2025-12-23
Branch: 001-outer-layout-config

## Decisions

- Config scope: Per-region only (sidebar.*, navbar.*). No top-level `navigation.*`.
- Navigation placement rules:
  - If `sidebar.show_at` is False/None → navbar-only mode; navbar menu may show at `navbar.menu_visible_at`.
  - If `sidebar.show_at` ∈ {sm, md, lg, xl, xxl} → primary nav always in sidebar; navbar menu never shows.
- Cotton integration: Use `:attrs` to pass dicts for `sidebar` and `navbar`, and pass brand/actions explicitly where needed.
- Accessibility: Ensure ARIA landmarks and focus order; collapsing sidebar retains accessible navigation and focus management.
- CSS independence: Layout CSS is namespaced and independent of any framework; component libraries (e.g., django-cotton-bs5) provide visual styling.
- Client behavior: Optional TypeScript for toggles; ship compiled JS; progressive enhancement so core navigation works without JS.

## Rationale

- Per-region config aligns with template usage, reduces ambiguity, and is intuitive for users editing templates.
- Single-source navigation rendering avoids cognitive load and duplication across regions.
- Template-only inner layout respects constitution and keeps customization discoverable.

## Alternatives Considered

- Global `navigation.*` defaults with overrides: Rejected for this feature to reduce surface area and confusion.
- `layout.breakpoints` object: Over-structures the schema for current needs; can be revisited if complexity grows.

## Open Questions

- None at this time.
