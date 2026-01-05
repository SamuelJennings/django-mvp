# Implementation Plan: AdminLTE Layout Component Separation

**Branch**: `001-layout-component-split` | **Date**: January 5, 2026 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-layout-component-split/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Split the monolithic AdminLTE layout template into 5 independent Cotton components (wrapper, header, sidebar, main, footer) to enable granular customization and flexible composition. Components use Cotton's c-vars for configuration and slots for content injection, maintaining AdminLTE 4's grid-based layout structure while providing 100% isolation between sections. Header, sidebar, and main components use subdirectory structure with sub-components for enhanced reusability.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Django 4.2+, django-cotton (Cotton component system with c-vars and slots)
**Storage**: N/A (template-only feature)
**Testing**: pytest with Django template rendering (render_to_string)
**Target Platform**: Django web applications (server-side rendered templates)
**Project Type**: Django package (django-mvp) providing AdminLTE 4 components
**Performance Goals**: Template rendering overhead <5ms per component, no impact on page load time
**Constraints**: Must maintain backward compatibility with existing mvp/base.html template blocks; Zero CSS/JavaScript changes to AdminLTE 4; All components must follow django-cotton snake_case naming convention
**Scale/Scope**: 5 main components (wrapper, header, sidebar, main, footer) + 6 sub-components (header/toggle, sidebar/branding, sidebar/menu, main/content_header, main/content) = 11 total template files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Version**: 1.0.0 (Ratified: 2026-01-05)

### Initial Check (Pre-Phase 0)

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Test-First** | ✅ PASS | Spec includes FR-013 requiring testable components; plan includes pytest coverage for all components |
| **II. Documentation-First** | ✅ PASS | Phase 1 generates quickstart.md with usage examples; all c-vars and slots will be documented |
| **III. Component Quality** | ✅ PASS | Components preserve AdminLTE's semantic HTML (FR-009); accessibility maintained from existing layout |
| **IV. Compatibility** | ✅ PASS | FR-010 mandates backward compatibility with existing mvp/base.html template blocks; config-driven via c-vars |
| **V. Tooling** | ✅ PASS | All tests run via `poetry run pytest`; standard project tooling (Ruff, djlint) |

**Quality Gates**:

- ✅ Unit/integration tests planned for all 10 components
- ✅ Linting/formatting via Ruff and djlint
- ✅ Documentation in Phase 1 (quickstart.md + component reference)
- ⚠️ **Deferred**: pytest-playwright coverage (existing implementation has no browser tests; maintaining current scope)

**Overall**: ✅ **PASS** - Feature aligns with all core principles. Will re-check after Phase 1 design.

---

### Post-Phase 1 Check (After Design)

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Test-First** | ✅ PASS | research.md documents testing strategy (render_to_string); 10 components × 3-5 tests = ~40 unit tests + integration tests |
| **II. Documentation-First** | ✅ PASS | quickstart.md complete with component reference, c-vars, slots, and usage examples; data-model.md documents component structure |
| **III. Component Quality** | ✅ PASS | data-model.md confirms semantic HTML preserved; snake_case naming follows django-cotton conventions |
| **IV. Compatibility** | ✅ PASS | research.md confirms backward compatibility strategy: all existing template blocks preserved in mvp/base.html |
| **V. Tooling** | ✅ PASS | Agent context updated with Python 3.11+, Django 4.2+, django-cotton; standard tooling (Poetry, Ruff, djlint) |

**Quality Gates**:

- ✅ Test strategy defined: pytest with render_to_string for all 11 components
- ✅ Documentation complete: quickstart.md (component reference), data-model.md (structure), research.md (decisions)
- ✅ Linting/formatting: djlint for templates, Ruff for Python (if needed)
- ⚠️ **Deferred**: pytest-playwright (maintaining scope - no browser tests in existing implementation)

**Overall**: ✅ **PASS** - Design phase complete. All principles satisfied. Ready for Phase 2 (tasks.md generation via /speckit.tasks).

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
mvp/
├── templates/
│   ├── mvp/
│   │   └── base.html                    # [MODIFIED] Updated to use new components
│   └── cotton/
│       └── app/
│           ├── wrapper.html              # [NEW] Top-level grid container
│           ├── footer.html               # [NEW] Footer component
│           ├── header/                   # [NEW] Header subdirectory
│           │   ├── index.html           # Header orchestrator with navbar
│           │   └── toggle.html          # Sidebar toggle button
│           ├── sidebar/                  # [NEW] Sidebar subdirectory
│           │   ├── index.html           # Sidebar orchestrator
│           │   ├── branding.html        # Logo and brand text
│           │   └── menu.html            # Navigation menu wrapper
│           └── main/                     # [NEW] Main content subdirectory
│               ├── index.html           # Main content orchestrator
│               ├── content_header.html  # Page title/breadcrumbs
│               └── content.html         # Main content wrapper
│
└── static/
    └── (no changes - CSS/JS preserved)

tests/
├── test_app_components.py               # [NEW] Unit tests for 11 component files
└── test_base_template_integration.py    # [NEW] Integration tests for mvp/base.html

example/
└── templates/
    └── example/
        └── dashboard.html               # [PRESERVED] Existing example, no changes
```

**Structure Decision**: Django package structure (Option 1 variant). This is a template-only feature with no Python models, services, or APIs. All changes are in `mvp/templates/cotton/app/` (11 new template files) and `mvp/templates/mvp/base.html` (1 modified file). Tests are co-located in `tests/` directory following existing project conventions.

## Complexity Tracking

**Status**: N/A - No constitution violations to justify.
