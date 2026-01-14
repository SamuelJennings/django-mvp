# Implementation Plan: AdminLTE Layout Configuration System

**Branch**: `002-layout-configuration` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-layout-configuration/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command.

## Summary

Primary requirement: Support AdminLTE's various layout options (fixed sidebar, header, footer) through configuration-driven design using boolean attributes on Cotton components. **SOLUTION**: Move `<body>` tag into `<c-app>` component and apply layout classes directly to body using Cotton's existing attribute system. Add JavaScript slot for user-provided scripts.

## Technical Context

**Language/Version**: Python 3.11, Django 5.1+
**Primary Dependencies**: django-cotton (template components), AdminLTE 4 (CSS framework)
**Storage**: N/A (configuration-driven layout, no data persistence)
**Testing**: pytest-django (component rendering), pytest-playwright (layout behavior)
**Target Platform**: Web browsers (responsive design, multiple viewports)
**Project Type**: Django package - extends existing django-mvp template system
**Performance Goals**: Zero runtime performance impact (CSS-only layout changes)
**Constraints**: Layout classes MUST be on `<body>` tag for AdminLTE compatibility
**Scale/Scope**: 4 layout variations (default + 3 fixed combinations), single demo page for testing

**Simple Cotton Architecture**: Move `<body>` tag into `<c-app>` component template with layout classes applied directly using Cotton's existing attribute handling. Add `{{ javascript }}` slot in component for user scripts.

## Constitution Check (Post-Design Re-evaluation)

*GATE: Re-check after Phase 1 design completion.*

- ✅ **Test-first approach remains feasible**: Tests can be written first for Cotton component
- ✅ **Test types simplified**:
  - **Component Tests**: Cotton component rendering with `django_cotton.render_component()`
  - **Browser Tests**: pytest-playwright for visual layout verification
- ✅ **Documentation scope clarified**: Simple Cotton component usage documented
- ✅ **Quality gates confirmed**: pytest + ruff lint/format

**Architecture Validation**: Simple Cotton approach eliminates complex infrastructure while providing correct AdminLTE compatibility. Body tag moved into component with layout classes applied directly.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
mvp/                                    # Core Django app
├── templates/
│   ├── cotton/
│   │   └── app/
│   │       └── index.html             # MODIFIED: Move body tag into component with layout classes
│   └── base.html                      # MODIFIED: Remove body tag, use c-app with javascript slot
└── # No new Python code needed - pure Cotton template solution

example/                               # Demo Django app
├── templates/
│   └── example/
│       └── layout_demo.html          # NEW: Demo page testing layout combinations
├── views.py                          # MODIFIED: Add simple demo view
└── urls.py                           # MODIFIED: Add demo URL

tests/
└── test_layout_components.py         # NEW: Cotton component layout tests
```

**Structure Decision**: Simple Cotton-only solution requiring minimal changes. No context processors, template tags, or utility modules needed. Layout logic embedded directly in Cotton component template using existing attribute system.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
