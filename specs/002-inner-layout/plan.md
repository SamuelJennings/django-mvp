# Implementation Plan: Inner Layout Component

**Branch**: `002-inner-layout` | **Date**: 2025-12-23 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-inner-layout/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Inner Layout Component provides a flexible multi-column layout system for Django-Cotton templates, enabling developers to compose content pages with optional primary_sidebar (left) and secondary_sidebar (right) slots. The component uses the default unnamed slot for main content and automatically expands content to fill available space when sidebars are absent. Responsive behavior includes switching sidebars to offcanvas mode below the `md` breakpoint (768px) and optional collapse mode (width reduction to fit-content) for icon-based navigation. Configuration is provided via data attributes on the component tag, with defaults of 280px for primary_sidebar and 250px for secondary_sidebar.

## Technical Context

**Language/Version**: Python 3.10-3.12  
**Primary Dependencies**: Django 4.2-5.x, django-cotton ≥2.3.1, django-cotton-bs5 ^0.5.1, Bootstrap 5.3, django-compressor ^4.5.1, django-libsass ^0.9  
**Storage**: N/A (component library)  
**Testing**: pytest ^8.0.0, pytest-django ^4.9.0  
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge) on mobile/tablet/desktop  
**Project Type**: Django package - provides reusable templates, SCSS, and JavaScript for inner content layout  
**Performance Goals**: Responsive layout transitions, no layout shift on initial load  
**Constraints**: Must work within outer layout system (feature 001), must not require external bundler for end users, must be accessible (WCAG 2.1 Level AA), compiled JS must ship with package  
**Scale/Scope**: Single component with 2-3 named slots, ~200 lines of SCSS, ~150 lines of TypeScript (compiled to JS), integration with existing Cotton ecosystem

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gate A: No duplicate navigation across navbar/sidebar for selected mode**
- Status: ✅ **PASS** - N/A for inner layout (does not handle navigation, only content regions)

**Gate B: Layout renders without any CSS framework present**
- Status: ✅ **PASS** - Inner layout structure uses custom namespaced classes (.content-shell, .content-sidebar-left, .content-sidebar-right, .content-main) independent of Bootstrap. Bootstrap classes are optional enhancements.

**Gate C: Inner layout regions reflect template attributes only**
- Status: ✅ **PASS** - Design explicitly uses Django-Cotton component with slot-based API. No configuration in settings or view mixins. All layout decisions happen in templates via component tag and slot declarations.

**Gate D: Basic accessibility landmarks and keyboard focus order present**
- Status: ✅ **PASS** (Post-Design Verification) - data-model.md §5.2 specifies ARIA landmarks:
  - Main content: `<div class="content-main" role="main" aria-label="Main content">`
  - Primary sidebar: `<div class="content-sidebar-left" role="complementary" aria-label="Primary navigation">`
  - Secondary sidebar: `<div class="content-sidebar-right" role="complementary" aria-label="Secondary information">`
  - Offcanvas mode: `role="dialog" aria-modal="true" aria-labelledby="offcanvas-title"`
  - Tab order preserved (sidebars before main content, collapse toggles properly labeled)
  - Focus management in javascript-api.md §2.6 (focus moved to offcanvas on open, returned to trigger on close)

**Gate E: Theming works via both Sass (build-time) and CSS variables (runtime)**
- Status: ✅ **PASS** - data-model.md §4.1 defines CSS variables (--content-primary-width, --content-secondary-width) for runtime theming. SCSS will provide build-time defaults. Component accepts width parameters that set CSS variables at runtime.

**Gate F: Compiled JS assets present and functional without external bundler**
- Status: ✅ **PASS** (Post-Design Verification) - javascript-api.md specifies:
  - JavaScript source at mvp/static/js/inner_layout.js (TypeScript optional for type safety)
  - Compiled/minified via django-compressor to ES5/ES6 bundle
  - Ships with package, no external bundler required by end users
  - Progressive enhancement: Core layout works without JS (data-model.md §5.1)
  - Bootstrap 5.3 offcanvas included in base template (no additional bundler required)
  - InnerLayoutManager class provides programmatic API (optional)

**Overall Status**: ✅ **FULL PASS** - All six constitution gates pass after Phase 1 design review. No violations. Design adheres to project principles:
  - Template-first approach (Gate C)
  - Progressive enhancement (Gate F core layout without JS)
  - Accessibility built-in (Gate D ARIA landmarks, keyboard navigation)
  - Flexible theming (Gate E CSS variables + SCSS)
  - No framework lock-in (Gate B custom classes, Bootstrap optional)

## Project Structure

### Documentation (this feature)

```text
specs/002-inner-layout/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── component-api.md # Component slot and attribute contract
│   ├── css-classes.md   # CSS class naming and behavior contract
│   └── javascript-api.md # JS API for collapse/offcanvas behavior
├── checklists/
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
mvp/
├── templates/
│   └── cotton/
│       └── layouts/
│           ├── inner.html          # Main inner layout component (EXISTS - will enhance)
│           └── sidebar.html        # OUT OF SCOPE (sidebar components separate spec)
├── static/
│   ├── scss/
│   │   ├── _content-layout.scss    # Inner layout styles (EXISTS - will enhance)
│   │   ├── _backwards-compat.scss  # Legacy class aliases (EXISTS - maintain)
│   │   └── stylesheet.scss         # Main SCSS entry point (EXISTS)
│   └── js/
│       ├── inner_layout.js         # Collapse/offcanvas behavior (EXISTS - will enhance)
│       └── inner_layout.ts         # TypeScript source (TO CREATE)
│
tests/
├── test_inner_layout_component.py  # Component rendering tests (TO CREATE)
├── test_inner_layout_responsive.py # Responsive behavior tests (TO CREATE)
└── test_inner_layout_slots.py      # Slot handling tests (TO CREATE)
│
docs/
└── INNER_LAYOUT.md                 # Component documentation (TO CREATE)
```

**Structure Decision**: Django package layout with templates, SCSS, and compiled JavaScript. The inner layout component already exists at `mvp/templates/cotton/layouts/inner.html` with basic structure but requires enhancement for:
1. Offcanvas mode at md breakpoint
2. Collapse mode with constraint enforcement
3. Empty slot detection and handling
4. Data attribute configuration API
5. ARIA landmarks and accessibility
6. TypeScript-based behavior compilation

Existing SCSS at `mvp/static/scss/_content-layout.scss` provides foundational styles with CSS variables and collapse transitions but needs offcanvas integration and responsive breakpoint logic.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitution violations. All gates pass.

---

## Phase 0: Research (Completed)

**Output**: [research.md](research.md)

**Summary**: Analyzed existing inner layout implementation (~40-53% complete), identified critical gaps (offcanvas mode, empty slot detection, wrong breakpoint/widths), researched Bootstrap offcanvas patterns, and documented design decisions for collapse constraints and empty slot handling.

**Key Findings**:
1. Existing implementation at mvp/templates/cotton/layouts/inner.html has basic structure with primary_sidebar/secondary_sidebar slots
2. Critical gaps: No offcanvas mode, breakpoint at 991px (should be 768px), widths at 250px (should be 280px primary/250px secondary)
3. Bootstrap 5.3 provides native .offcanvas-{breakpoint} classes - no custom media queries needed
4. Slot detection via Cotton: `{% if slot %}` - slots are truthy when declared in template
5. Data attributes should set CSS variables for runtime theming
6. Collapse constraint: Cannot collapse when in offcanvas mode (requires JavaScript enforcement)

**Decisions Made**:
- Use Bootstrap .offcanvas-md for responsive behavior at 768px
- Use Cotton's native slot detection (slots truthy when declared)
- Use data attributes (data-primary-width, etc.) to set CSS variables
- Enforce collapse constraint via JavaScript (prevent collapse in offcanvas mode)

---

## Phase 1: Design (Completed)

### Data Model

**Output**: [data-model.md](data-model.md)

**Summary**: Defines component structure with 3 slots (default/primary_sidebar/secondary_sidebar), 6 data attributes for configuration, CSS variables schema, and 4-state machine (NORMAL/COLLAPSED/OFFCANVAS/OFFCANVAS OPEN).

**Key Components**:
- **Slots**: Default (main content), primary_sidebar (left), secondary_sidebar (right)
- **Data Attributes**: data-primary-width, data-secondary-width, data-breakpoint, data-gap, data-collapse-primary, data-collapse-secondary
- **CSS Variables**: --content-primary-width, --content-secondary-width
- **State Machine**: 4 states with transition rules and collapse constraint enforcement

### API Contracts

**Output**: [contracts/](contracts/)

**Summary**: Three contract documents establishing stable APIs with semantic versioning commitments.

**Component API** ([component-api.md](contracts/component-api.md)):
- Component signature: `<c-layouts.inner>` with 7 optional parameters
- 3 slots: default (unnamed), primary_sidebar, secondary_sidebar
- Contract guarantees: empty slot handling, responsive behavior, collapse constraint, accessibility
- Usage examples: minimal, single sidebar, dual sidebar, full customization

**CSS Classes** ([css-classes.md](contracts/css-classes.md)):
- 9 public CSS classes: .content-shell, .content-sidebar-left, .content-sidebar-right, .content-main, .collapse-toggle, .collapsed, .collapsible, .collapsed-only, .expanded-only
- 2 public CSS variables: --content-primary-width, --content-secondary-width
- Backwards compatibility: .inner-* classes aliased (deprecated)
- Testing: CSS class presence tests defined

**JavaScript API** ([javascript-api.md](contracts/javascript-api.md)):
- InnerLayoutManager class with constructor(options)
- 7 public methods: init, toggleCollapse, isCollapsed, isOffcanvasMode, expandSidebar, collapseSidebar, destroy
- 3 custom events: innerlayout:collapsed, innerlayout:expanded, innerlayout:offcanvasmode
- localStorage schema: innerlayout_primary_collapsed, innerlayout_secondary_collapsed
- Progressive enhancement: Core layout works without JS
- TypeScript type exports for editor autocomplete

### Quick Start Guide

**Output**: [quickstart.md](quickstart.md)

**Summary**: Developer quick-start guide with usage examples, customization patterns, and troubleshooting.

**Contents**:
- Basic usage: Simple content, single sidebar, dual sidebar
- Customization: Custom widths, breakpoints, gap, collapsible sidebars
- Common patterns: Documentation layout, blog post, dashboard, list/detail view
- Responsive behavior: Desktop vs mobile
- Accessibility: ARIA landmarks, keyboard navigation
- JavaScript API: Optional programmatic control
- Troubleshooting: Empty slots, collapse constraints, custom widths

### Agent Context Update

**Output**: Updated [.github/agents/copilot-instructions.md](.github/agents/copilot-instructions.md)

**Summary**: Added inner layout technologies and patterns to GitHub Copilot instructions.

**Changes**:
- Added language: Python 3.10-3.12
- Added frameworks: Django 4.2-5.x, django-cotton ≥2.3.1, django-cotton-bs5 ^0.5.1, Bootstrap 5.3
- Added database: N/A (component library)
- Preserved manual context between markers

---

## Next Steps

**Command Completed**: `/speckit.plan` has finished Phase 0 (research) and Phase 1 (design).

**To Continue Implementation**:
1. Run `/speckit.tasks` to generate implementation tasks from this design
2. Tasks will be broken down into atomic units for implementation
3. Implement in order: Templates → SCSS → TypeScript → Tests → Documentation

**Branch**: `002-inner-layout`  
**Spec**: [spec.md](spec.md)  
**Plan**: [plan.md](plan.md) (this file)
