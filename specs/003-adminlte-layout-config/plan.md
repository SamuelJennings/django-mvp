# Implementation Plan: AdminLTE Layout Configuration System

**Branch**: `003-adminlte-layout-config` | **Date**: 2026-01-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-adminlte-layout-config/spec.md`

## Summary

Implement AdminLTE 4's layout configuration system in django-mvp, allowing developers to control fixed vs scrolling behavior for sidebar, header, and footer elements via Cotton component attributes. This includes:

- Boolean attributes on `<c-app>` component (fixed_sidebar, fixed_header, fixed_footer)
- Responsive sidebar expansion breakpoints (sm, md, lg, xl, xxl)
- CSS class generation matching AdminLTE 4 conventions
- Demo views in example/ app for testing layout combinations and responsive behavior

Technical approach: Extend existing `<c-app>` Cotton component to accept layout attributes, generate appropriate body classes, and provide interactive demo views with forms/dropdowns for testing all combinations.

## Technical Context

**Language/Version**: Python 3.10-3.12
**Primary Dependencies**: Django 4.2-5.x, django-cotton >=2.3.1, AdminLTE 4 (CSS via CDN)
**Storage**: N/A (no database changes - template/static files only)
**Testing**: pytest, pytest-django (component rendering tests)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Django reusable app package
**Performance Goals**: <50ms additional page load time for fixed layouts (per SC-005)
**Constraints**:

- Must maintain AdminLTE 4 CSS class naming conventions
- Must not break existing layouts/templates
- Must work with django-cotton's attribute/slot system
- Fixed elements must work correctly with 10,000+ lines of scrollable content
**Scale/Scope**: Single Cotton component modification + 2 demo views + tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Test-first approach is feasible and planned**

- Tests can be written first for component attribute handling
- Tests for CSS class generation based on attributes
- Tests for demo view query parameter handling
- Tests for rendered HTML structure with various layout combinations

✅ **Test types are identified**

- pytest-django for Cotton component rendering tests using `render_component()`
- pytest-django for demo view integration tests
- Unit tests for CSS class generation logic
- No pytest-playwright needed (layout behavior is pure CSS, not JS interactions)

✅ **Documentation updates are included**

- Update component documentation with layout attributes
- Document sidebar_expand breakpoint options
- Add examples for each layout combination
- Document demo views for testing

✅ **Quality gates are understood**

- All tests pass via `poetry run pytest`
- Ruff linting passes
- Ruff formatting applied
- djlint for template formatting

---

### Post-Design Re-Evaluation (Phase 1 Complete)

✅ **Test-First Compliance**

- All functionality is testable via pytest-django component rendering
- Demo views can be tested with Django test client
- No untestable browser-specific behavior (AdminLTE CSS handles all visual effects)
- Clear test cases documented in [contracts/component-api.md](./contracts/component-api.md)

✅ **Documentation-First Compliance**

- [quickstart.md](./quickstart.md) provides developer-facing usage guide
- [contracts/component-api.md](./contracts/component-api.md) defines complete API contract
- [data-model.md](./data-model.md) explains configuration model
- All public behavior documented with examples

✅ **Component Quality & Accessibility**

- No HTML structure changes (uses existing AdminLTE structure)
- Layout configuration is pure CSS classes (no accessibility impact)
- Demo views will use semantic HTML with proper ARIA attributes
- Fixed positioning is CSS-only (fully accessible)

✅ **Compatibility & Config-Driven Design**

- Component attribute approach is config-driven (no template overrides needed)
- Backward compatible - existing templates without attributes continue to work
- No breaking changes to `<c-app>` component API (only additions)
- Default behavior (no attributes) remains unchanged

✅ **No Constitution Violations**

All core principles satisfied. Design is ready for implementation.

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
└── templates/
    └── cotton/
        └── app.html           # MODIFY: Add layout attribute handling

example/
├── views.py                    # ADD: Demo views for layout testing
├── urls.py                     # MODIFY: Add demo view URLs
└── templates/
    └── example/
        ├── layout_fixed.html   # ADD: Fixed properties demo page
        └── layout_responsive.html  # ADD: Responsive breakpoint demo page

tests/
├── test_app_layout.py          # ADD: Component layout attribute tests
├── test_layout_demo_views.py   # ADD: Demo view integration tests
└── conftest.py                 # MODIFY: Add fixtures if needed

docs/
└── components/
    └── app.md                  # MODIFY: Document layout attributes
```

**Structure Decision**: This is a Django reusable app package. Changes are localized to:

1. Core component (`mvp/templates/cotton/app.html`) - add attribute handling
2. Example app (`example/`) - add demo views and templates
3. Tests (`tests/`) - add comprehensive test coverage
4. Documentation (`docs/`) - update component reference

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
