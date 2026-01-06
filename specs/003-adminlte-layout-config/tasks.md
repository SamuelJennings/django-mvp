# Implementation Tasks: AdminLTE Layout Configuration System

**Feature**: 003-adminlte-layout-config
**Branch**: `003-adminlte-layout-config`
**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)
**Updated**: 2026-01-06

## Task Summary

- **Total Tasks**: 41
- **Setup**: 1 task (completed)
- **Foundational**: 0 tasks (component already exists)
- **User Story 1** (Apply Basic Layout Variations - P1): 5 tasks (completed)
- **User Story 2** (Combine Multiple Fixed Elements - P2): 3 tasks (completed)
- **User Story 3** (Configure Layout Per-Page - P3): 2 tasks (completed)
- **Demo Views** (Testing Infrastructure - FR-010 to FR-014): 15 tasks (completed)
- **Documentation**: 8 tasks (completed)
- **Polish & Cross-Cutting**: 5 tasks (completed)
- **Final Validation**: 2 tasks (1 pending)

## Implementation Strategy

**Status**: Core component implementation complete. Demo views implemented. Remaining work: Manual browser validation (T022).

**Test-First Approach**: Following Django MVP constitution, all tests written and observed failing before implementation.

**Demo Views Purpose**: Interactive testing pages for validating layout behavior without requiring browser automation tests.

---

## Phase 1: Setup

### Environment Setup

- [X] T001 Verify pytest-django test environment configured in tests/settings.py

---

## Phase 2: User Story 1 - Apply Basic Layout Variations (P1)

**Goal**: Test that individual fixed attributes render correct AdminLTE CSS classes

**Independent Test Criteria**: Each fixed attribute (fixed_sidebar, fixed_header, fixed_footer) can be tested independently by verifying the correct CSS class appears on the body element.

### Tests

- [X] T002 [P] [US1] Write test for fixed_sidebar attribute renders .layout-fixed class in tests/test_app_component.py
- [X] T003 [P] [US1] Write test for fixed_header attribute renders .fixed-header class in tests/test_app_component.py
- [X] T004 [P] [US1] Write test for fixed_footer attribute renders .fixed-footer class in tests/test_app_component.py
- [X] T005 [P] [US1] Write test for default (no attributes) renders no fixed classes in tests/test_app_component.py

### Validation

- [X] T006 [US1] Run all User Story 1 tests and verify existing <c-app> implementation passes (validates FR-001, FR-002, FR-003, FR-006)

---

## Phase 3: User Story 2 - Combine Multiple Fixed Elements (P2)

**Goal**: Test that multiple fixed attributes work together correctly

**Independent Test Criteria**: Multiple fixed attributes can be enabled simultaneously and all corresponding CSS classes appear on the body element.

### Tests

- [X] T007 [P] [US2] Write test for fixed_sidebar + fixed_header combination renders both classes in tests/test_app_component.py
- [X] T008 [P] [US2] Write test for fixed_header + fixed_footer combination renders both classes in tests/test_app_component.py
- [X] T009 [P] [US2] Write test for fixed_sidebar + fixed_header + fixed_footer (complete) renders all three classes in tests/test_app_component.py

---

## Phase 4: User Story 3 - Configure Layout Per-Page or Globally (P3)

**Goal**: Test that layout attributes work with Django template inheritance

**Independent Test Criteria**: Child templates can override layout attributes from parent templates, and the override takes precedence.

### Tests

- [X] T010 [US3] Write test for template inheritance with base template having fixed_sidebar in tests/test_app_component.py
- [X] T011 [US3] Write test for attribute override in child template renders overridden layout in tests/test_app_component.py

---

## Phase 5: Documentation

### Component Documentation

- [X] T012 [P] Create docs/components/app.md with <c-app> component reference
- [X] T013 [P] Document fixed_sidebar attribute with examples in docs/components/app.md
- [X] T014 [P] Document fixed_header attribute with examples in docs/components/app.md
- [X] T015 [P] Document fixed_footer attribute with examples in docs/components/app.md
- [X] T016 [P] Document sidebar_expand attribute interaction in docs/components/app.md

### Project Documentation

- [X] T017 Add layout configuration section to README.md with quickstart example
- [X] T018 Update CHANGELOG.md with layout feature documentation

---

## Phase 6: Polish & Cross-Cutting Concerns

### Edge Case Testing

- [X] T019 [P] Write test for custom class attribute doesn't conflict with fixed classes in tests/test_app_component.py

---

## Phase 7: Interactive Demo Views (FR-010 to FR-014)

**Goal**: Create interactive demo views for testing fixed properties and responsive breakpoints per spec clarifications

**Independent Test Criteria**: Demo views can be accessed via URLs and allow dynamic testing of layout configurations via query parameters

### Fixed Properties Demo View

- [X] T027 [P] [DEMO] Write test for layout_fixed_demo view with no query params in tests/test_layout_demo_views.py
- [X] T028 [P] [DEMO] Write test for layout_fixed_demo view with fixed_sidebar=on query param in tests/test_layout_demo_views.py
- [X] T029 [P] [DEMO] Write test for layout_fixed_demo view with all checkboxes (fixed_sidebar+fixed_header+fixed_footer) in tests/test_layout_demo_views.py
- [X] T030 [DEMO] Implement layout_fixed_demo view in example/views.py that parses query params
- [X] T031 [DEMO] Create example/templates/example/layout_fixed.html with checkbox form
- [X] T032 [P] [DEMO] Add long-form content (2-3 viewport heights) to layout_fixed.html template
- [X] T033 [P] [DEMO] Add 12-15 dummy sidebar menu items to layout_fixed.html template
- [X] T034 [P] [DEMO] Add helper text and visual status indicators to layout_fixed.html template

### Responsive Breakpoint Demo View

- [X] T035 [P] [DEMO] Write test for layout_responsive_demo view with default breakpoint in tests/test_layout_demo_views.py
- [X] T036 [P] [DEMO] Write test for layout_responsive_demo view with breakpoint=md query param in tests/test_layout_demo_views.py
- [X] T037 [DEMO] Implement layout_responsive_demo view in example/views.py with breakpoint validation
- [X] T038 [DEMO] Create example/templates/example/layout_responsive.html with breakpoint dropdown
- [X] T039 [P] [DEMO] Add content sections and dummy sidebar items to layout_responsive.html template

### Demo View URLs

- [X] T040 [DEMO] Add /example/layout-fixed/ URL route in example/urls.py
- [X] T041 [DEMO] Add /example/layout-responsive/ URL route in example/urls.py

---

## Phase 8: Polish & Cross-Cutting Concerns

### Edge Case Testing

- [X] T019 [P] Write test for custom class attribute doesn't conflict with fixed classes in tests/test_app_component.py
- [X] T020 [P] Write test for sidebar_expand values (sm, md, lg, xl, xxl) render correct classes in tests/test_app_component.py
- [X] T020b [P] Write test for contradictory boolean attributes in tests/test_app_component.py

### Final Validation

- [X] T021 Run full test suite with coverage report and verify 100% coverage for app layout attributes
- [ ] T022 Manually verify cross-browser rendering (Chrome, Firefox, Safari, Edge) using demo views per SC-002

---

## Dependency Graph

```mermaid
graph TD
    T001[T001: Setup] --> T002[T002: US1 Tests]
    T001 --> T003[T003: US1 Tests]
    T001 --> T004[T004: US1 Tests]
    T001 --> T005[T005: US1 Tests]

    T002 --> T006[T006: US1 Validation]
    T003 --> T006
    T004 --> T006
    T005 --> T006

    T006 --> T007[T007: US2 Tests]
    T006 --> T008[T008: US2 Tests]
    T006 --> T009[T009: US2 Tests]

    T006 --> T010[T010: US3 Tests]
    T006 --> T011[T011: US3 Tests]

    T006 --> T012[T012: Component Docs]
    T012 --> T013[T013: Doc fixed_sidebar]
    T012 --> T014[T014: Doc fixed_header]
    T012 --> T015[T015: Doc fixed_footer]
    T012 --> T016[T016: Doc sidebar_expand]

    T013 --> T017[T017: README]
    T014 --> T017
    T015 --> T017
    T016 --> T017

    T017 --> T018[T018: CHANGELOG]

    T006 --> T019[T019: Edge Cases]
    T006 --> T020[T020: Breakpoint Tests]
    T006 --> T020b[T020b: Contradictory Attrs]

    %% Demo Views
    T006 --> T027[T027: Fixed Demo Test 1]
    T006 --> T028[T028: Fixed Demo Test 2]
    T006 --> T029[T029: Fixed Demo Test 3]
    T027 --> T030[T030: Fixed Demo View]
    T028 --> T030
    T029 --> T030
    T030 --> T031[T031: Fixed Demo Template]
    T031 --> T032[T032: Add Content]
    T031 --> T033[T033: Add Sidebar Items]
    T031 --> T034[T034: Add Helper Text]
    
    T006 --> T035[T035: Responsive Demo Test 1]
    T006 --> T036[T036: Responsive Demo Test 2]
    T035 --> T037[T037: Responsive Demo View]
    T036 --> T037
    T037 --> T038[T038: Responsive Demo Template]
    T038 --> T039[T039: Add Content to Template]
    
    T030 --> T040[T040: Add Fixed URL]
    T037 --> T041[T041: Add Responsive URL]
    
    T007 --> T021[T021: Final Validation]
    T008 --> T021
    T009 --> T021
    T010 --> T021
    T011 --> T021
    T019 --> T021
    T020 --> T021
    T020b --> T021
    T018 --> T021
    
    T034 --> T022[T022: Browser Validation]
    T039 --> T022
    T040 --> T022
    T041 --> T022
    T021 --> T022
        context=RequestContext(rf.get("/"), {"fixed_sidebar": True})
    )
    assert 'class="bg-body-tertiary layout-fixed' in html
    assert '<div class="app-wrapper">' in html
    assert 'sidebar-expand-lg' in html  # Default value
```

### Coverage Goals

- 100% coverage for layout attribute logic in `<c-app>` component
- All attribute combinations tested
- Edge cases covered (custom classes, breakpoint values)

## Success Criteria

- ✅ Core component tests complete (T001-T021)
- ✅ Documentation complete (T012-T018)
- [ ] Demo views implemented and tested (T027-T041)
- [ ] Manual cross-browser validation complete (T022)
- ✅ Test suite passes with 100% coverage for layout attributes
- ✅ No ruff linting errors
- ✅ CHANGELOG updated

## Notes

**Implementation Status**: The `<c-app>` component in `mvp/templates/cotton/app/index.html` already implements all layout attributes (T001-T021 complete). 

**Remaining Work**: Demo views (T027-T041) to provide interactive testing interface per spec requirements (FR-010 to FR-014).

**Demo Views Purpose**:
- **Fixed Properties Demo** (`/example/layout-fixed/`): Interactive form with checkboxes to test all fixed attribute combinations
- **Responsive Breakpoint Demo** (`/example/layout-responsive/`): Dropdown selector to test sidebar expansion at different breakpoints  
- **Benefits**: Manual validation without browser automation tests, shareable URLs for configurations, educational reference for developers

**MVP Focus**: Core functionality complete. Demo views enhance testing and documentation but are not required for library functionality.
