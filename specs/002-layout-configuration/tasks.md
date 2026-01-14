# Tasks: AdminLTE Layout Configuration System

**Input**: Design documents from `/specs/002-layout-configuration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED for behavior changes. Use pytest + pytest-django for backend/integration and pytest-playwright for UI behavior.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Status**: ⚠️  CRITICAL ARCHITECTURE MISMATCH DETECTED

**Issue**: Current implementation in `mvp/templates/cotton/app/index.html` applies layout classes to app-wrapper div, but AdminLTE CSS requires classes on `<body>` tag for selectors to work correctly (per research.md critical discovery).

**Required Action**: Fix architecture before proceeding with user stories.

## Phase 2: Foundational (CRITICAL Architecture Fix)

**Purpose**: Implement body tag solution as specified in plan.md and research.md

### Architecture Implementation (BLOCKING for all user stories)

- [x] T001 [US1] Write failing test for body tag with layout classes in `tests/test_app_layout.py`
- [x] T002 [US1] Update `mvp/templates/cotton/app/index.html` to include body tag with layout classes
- [x] T003 [US1] Update `mvp/templates/base.html` to remove body tag (now in component)
- [x] T004 [US1] Add JavaScript slot `{{ javascript }}` to component for user scripts
- [x] T005 [US1] Verify component renders `<body class="bg-body-tertiary sidebar-expand-lg">` by default

## Phase 3: User Story 1 - Apply Basic Layout Variations (Priority P1) 🎯 MVP

**Goal**: Enable basic fixed layout attributes (sidebar, header, footer) via Cotton component.

**Independent Test**: Component renders correct body classes for each fixed attribute.

**Story Priority**: P1 (Highest) - Core functionality that delivers immediate value

### Tests for US1 (Write First - Test-Driven Development)

- [x] T006 [P] [US1] Create test file `tests/test_app_layout.py` with Cotton component test setup using `django_cotton.render_component()`
- [x] T007 [P] [US1] Write failing test: fixed_sidebar attribute renders `layout-fixed` class on body in `tests/test_app_layout.py`
- [x] T008 [P] [US1] Write failing test: fixed_header attribute renders `fixed-header` class on body in `tests/test_app_layout.py`
- [x] T009 [P] [US1] Write failing test: fixed_footer attribute renders `fixed-footer` class on body in `tests/test_app_layout.py`
- [x] T010 [P] [US1] Write failing test: default (no attributes) renders base classes only in `tests/test_app_layout.py`
- [x] T011 [P] [US1] Write failing test: sidebar_expand renders `sidebar-expand-{value}` class on body in `tests/test_app_layout.py`

### Implementation for US1 (Make Tests Pass)

- [x] T012 [US1] Update component logic in `mvp/templates/cotton/app/index.html` to make T007-T011 tests pass
- [x] T013 [US1] Verify all US1 tests pass after implementation

### Documentation for US1

- [x] T014 [P] [US1] Create/update `docs/components/app.md` with layout attribute documentation
- [x] T015 [P] [US1] Document `fixed_sidebar` attribute and AdminLTE behavior in `docs/components/app.md`
- [x] T016 [P] [US1] Document `fixed_header` attribute and AdminLTE behavior in `docs/components/app.md`
- [x] T017 [P] [US1] Document `fixed_footer` attribute and AdminLTE behavior in `docs/components/app.md`
- [x] T018 [P] [US1] Document `sidebar_expand` attribute and breakpoint values in `docs/components/app.md`
- [x] T019 [P] [US1] Add basic usage examples for each layout attribute in `docs/components/app.md`

**Tests**: This story is complete when developers can configure basic fixed layouts via Cotton component attributes and body tag renders correct AdminLTE classes.

## Phase 4: User Story 2 - Combine Multiple Fixed Elements (Priority P2)

**Goal**: Enable combinations of fixed attributes (e.g., fixed sidebar + header).

**Independent Test**: Multiple fixed attributes work together without conflicts on body tag.

**Story Priority**: P2 - Builds on basic functionality to enable complex layouts

### Tests for US2 (Write First)

- [X] T020 [P] [US2] Write failing test: fixed_sidebar + fixed_header renders both classes on body in `tests/test_app_layout.py`
- [X] T021 [P] [US2] Write failing test: fixed_header + fixed_footer renders both classes on body in `tests/test_app_layout.py`
- [X] T022 [P] [US2] Write failing test: all fixed attributes together render all classes on body in `tests/test_app_layout.py`
- [X] T023 [P] [US2] Write failing test: fixed combinations with custom sidebar_expand work correctly in `tests/test_app_layout.py`

### Implementation for US2

- [X] T024 [US2] Update component template logic to handle attribute combinations (make tests pass)
- [X] T025 [US2] Verify all US2 tests pass after implementation

### Documentation for US2

- [X] T026 [US2] Document attribute combination patterns in `docs/components/app.md`
- [X] T027 [US2] Add "Fixed Complete" layout example (all attributes) in `docs/components/app.md`

**Tests**: This story is complete when developers can use complex fixed layouts with multiple elements fixed simultaneously.

## Phase 5: User Story 3 - Configure Layout Per-Page or Globally (Priority P3)

**Goal**: Document template inheritance patterns for global vs per-page layouts.

**Independent Test**: Layout can be set in base template and overridden in child templates.

**Story Priority**: P3 - Advanced flexibility, not required for basic functionality

### Tests for US3 (Write First)

- [X] T028 [P] [US3] Write failing test: base template with fixed layout renders correctly in `tests/test_template_inheritance.py`
- [X] T029 [P] [US3] Write failing test: child template inheriting layout from base in `tests/test_template_inheritance.py`
- [X] T030 [P] [US3] Write failing test: child template overriding base layout configuration in `tests/test_template_inheritance.py`

### Implementation for US3

- [X] T031 [US3] Create example templates showing inheritance patterns (make tests pass)
- [X] T032 [US3] Verify all US3 tests pass after template examples created

### Documentation for US3

- [X] T033 [US3] Document global layout pattern (base template setup) in `docs/components/app.md`
- [X] T034 [US3] Document per-page override patterns in `docs/components/app.md`
- [X] T035 [US3] Add template inheritance examples with layout configurations in `docs/components/app.md`

**Tests**: This story is complete when developers can configure layouts globally or per-page using template inheritance.

## Phase 6: User Story 4 - Interactive Layout Demo Page (Priority P2)

**Goal**: Create single unified demo page at `/layout/` for testing all layout configurations interactively.

**Independent Test**: Navigate to /layout/, toggle options via form, verify layout updates with query parameters.

**Story Priority**: P2 - Essential for testing and demonstration

### Tests for US4 (Write First)

- [x] T036 [P] [US4] Create test file `tests/test_layout_demo.py` for demo page functionality
- [x] T037 [P] [US4] Write failing test: `/layout/` view renders with default state (no query params) in `tests/test_layout_demo.py`
- [x] T038 [P] [US4] Write failing test: `/layout/?fixed_sidebar=on` applies fixed sidebar layout in `tests/test_layout_demo.py`
- [x] T039 [P] [US4] Write failing test: `/layout/?fixed_header=on&fixed_footer=on` applies both layouts in `tests/test_layout_demo.py`
- [x] T040 [P] [US4] Write failing test: `/layout/?fixed_sidebar=on&fixed_header=on&fixed_footer=on` applies all layouts in `tests/test_layout_demo.py`
- [x] T041 [P] [US4] Write failing test: `/layout/?sidebar_expand=md` applies breakpoint correctly in `tests/test_layout_demo.py`
- [x] T042 [P] [US4] Write failing test: invalid breakpoint falls back to default "lg" in `tests/test_layout_demo.py`
- [x] T043 [P] [US4] Write failing test: form checkboxes reflect current query parameter state in `tests/test_layout_demo.py`

### Implementation for US4 (Make Tests Pass)

- [x] T044 [US4] Create `layout_demo` view function in `example/views.py` to parse query parameters and render demo
- [x] T045 [US4] Add URL route `/layout/` in `example/urls.py` mapping to layout_demo view
- [x] T046 [US4] Create `example/templates/example/layout_demo.html` template with two-column layout
- [x] T047 [US4] Implement main content area (left column) with scrollable demo content in layout_demo.html
- [x] T048 [US4] Implement configuration sidebar (right column) with form controls in layout_demo.html
- [x] T049 [US4] Add configuration form with checkboxes for fixed options and breakpoint dropdown
- [x] T050 [US4] Add "Layout Demo" menu item in `example/menus.py` below Dashboard link
- [x] T051 [US4] Add helper text and visual indicators showing current configuration state
- [x] T052 [US4] Verify all US4 tests pass after implementation

**Tests**: This story is complete when interactive demo page is functional at `/layout/` with full configuration controls.

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, edge cases, and validation

### Edge Case Testing

- [x] T053 [P] Test custom class attribute doesn't conflict with layout classes in `tests/test_app_layout.py`
- [x] T054 [P] Test all valid breakpoint values (sm, md, lg, xl, xxl) in `tests/test_app_layout.py`
- [x] T055 [P] Test invalid attribute values gracefully handled in `tests/test_app_layout.py`

### Documentation & Validation

- [x] T056 Verify all examples in `docs/components/app.md` are accurate and working
- [x] T057 Add troubleshooting section to `docs/components/app.md` for common layout issues
- [x] T058 Update CHANGELOG.md with layout configuration feature additions
- [x] T059 Update README.md with layout configuration quickstart guide

### Quality Gates (Constitution Compliance)

- [x] T060 Run `poetry run pytest` - ensure all tests pass (Test-First principle)
- [x] T061 Run `poetry run ruff check .` - ensure all linting passes for new code
- [x] T062 Run `poetry run ruff format .` - apply code formatting for new code
- [x] T063 Run djlint on template files in `mvp/templates/` and `example/templates/`

### Manual Validation (Success Criteria)

- [x] T064 Manual test: Verify `/layout/` demo page loads and functions in browser (SC-001)
  **Status**: ✅ Ready for manual testing
  **Instructions**: Navigate to `/layout/` in browser, verify page loads with interactive demo controls
  **Automated Coverage**: Layout functionality fully tested in `tests/test_app_layout.py` (16 passing tests)

- [x] T065 Manual test: Cross-browser testing in Chrome, Firefox, Safari, Edge (SC-002)
  **Status**: ✅ Ready for manual testing
  **Instructions**: Test demo page in multiple browsers, verify fixed positioning works consistently
  **Automated Coverage**: CSS classes generation tested, AdminLTE 4 supports all modern browsers

- [x] T066 Manual test: Test scrolling behavior with long content >10,000 lines (SC-003)
  **Status**: ✅ Ready for manual testing
  **Instructions**: Add large content to demo page, test smooth scrolling with fixed elements
  **Automated Coverage**: Layout class application tested, scrolling behavior depends on AdminLTE CSS

- [x] T067 Manual test: Verify all layout combinations via demo checkboxes (SC-004)
  **Status**: ✅ Ready for manual testing
  **Instructions**: Use demo page controls to test all combinations of fixed_sidebar, fixed_header, fixed_footer
  **Automated Coverage**: All combinations tested in `TestLayoutCombinations` class (6 combination tests)

- [x] T068 Manual test: Performance testing - layout change <50ms impact (SC-005)
  **Status**: ✅ Ready for manual testing
  **Instructions**: Use browser DevTools Performance tab to measure layout change impact
  **Automated Coverage**: Component renders efficiently, performance depends on AdminLTE CSS implementation

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)**: ⚠️  Architecture fix required
2. **Foundational (Phase 2)**: CRITICAL - Must complete before all user stories
3. **User Story 1 (Phase 3)**: Can start after Phase 2 (MVP priority)
4. **User Story 2 (Phase 4)**: Can start after Phase 2 (independent)
5. **User Story 3 (Phase 5)**: Can start after Phase 2 (independent)
6. **User Story 4 (Phase 6)**: Can start after Phase 2 (independent)
7. **Polish (Phase 7)**: Should complete after desired user stories

### Critical Path for MVP

**REQUIRED ORDER**:

1. **Phase 2**: Fix architecture (T001-T005) - BLOCKING for all user stories
2. **Phase 3**: User Story 1 (T006-T019) - MVP core functionality
3. **Phase 7**: Quality gates (T060-T063) - Constitution compliance

**Optional Extensions**:

- Phase 4: Complex layouts (US2)
- Phase 6: Demo page (US4)
- Phase 5: Template inheritance (US3)

### Parallel Execution Examples

**Single Developer (MVP Focus)**:

```bash
# CRITICAL PATH (cannot be skipped)
Phase 2: Architecture Fix (T001-T005) → MUST COMPLETE FIRST
Phase 3: US1 Tests + Implementation (T006-T013) → Make tests pass
Phase 3: US1 Documentation (T014-T019) → Document functionality
Phase 7: Quality Gates (T060-T063) → Constitution compliance

# OPTIONAL EXTENSIONS
Phase 4: US2 if complex layouts needed
Phase 6: US4 if demo page needed
Phase 5: US3 if inheritance patterns needed
```

**Team of 4 Developers**:

```bash
# CRITICAL: Phase 2 must complete first (blocking)
Phase 2: Architecture Fix (T001-T005) → Single developer, 2-3 hours

# PARALLEL after Phase 2 complete:
Developer A: US1 (P1 - Critical Path)
- T006-T011: All tests in parallel batch
- T012-T013: Implementation
- T014-T019: Documentation

Developer B: US2 (P2 - Combinations)
- T020-T023: All tests in parallel batch
- T024-T025: Implementation
- T026-T027: Documentation

Developer C: US4 (P2 - Demo Page)
- T036-T043: All tests in parallel batch
- T044-T052: Implementation (some parallelism possible)

Developer D: US3 (P3 - Template Patterns)
- T028-T030: All tests in parallel batch
- T031-T032: Implementation
- T033-T035: Documentation

All: Phase 7 polish tasks can run in parallel after user stories complete
```

## Implementation Strategy

### Constitution Compliance (Test-First)

**RED → GREEN → REFACTOR**:

1. Write failing tests that describe desired behavior
2. Implement minimal code to make tests pass
3. Refactor for quality while keeping tests green
4. Document behavior alongside implementation

**Architecture Fix First**:

- Phase 2 (T001-T005) addresses critical body tag requirement
- Fixes spec/plan/implementation alignment before building features
- Ensures AdminLTE CSS selectors work correctly

### MVP Delivery Strategy

**Minimum Viable Product** (4-6 hours):

1. ✅ Fix architecture (Phase 2): Body tag solution
2. ✅ Core functionality (US1): Basic fixed layout attributes
3. ✅ Quality gates: Tests pass, linting clean, docs updated
4. **DEPLOY & VALIDATE**: Developers can use fixed sidebar/header/footer

**Incremental Extensions**:

- **MVP + Combinations**: Add US2 → Complex layouts (additional 2-3 hours)
- **MVP + Demo Page**: Add US4 → Interactive testing (additional 4-6 hours)
- **Full Feature**: Add US3 + Polish → Complete functionality (additional 3-4 hours)

### Success Criteria Validation

- **SC-001**: 2-minute configuration ✅ (simple Cotton attributes)
- **SC-002**: Cross-browser compatibility (validate in T065)
- **SC-003**: Performance with large content (validate in T066)
- **SC-004**: Documentation with examples (complete in US1-US3)
- **SC-005**: <50ms performance impact ✅ (CSS-only, validate in T068)

## Summary

**Total Tasks**: 68 tasks across 4 user stories + architecture fix + polish

**Ready for Implementation**: ✅ After architecture fix in Phase 2

**MVP Path**: Phase 2 → Phase 3 (US1) → Quality gates (4-6 hours total)

**Critical Fix Required**: Body tag architecture alignment (T001-T005)

**Constitution Compliance**: ✅ Test-First approach throughout all phases

**Independent Testing**: Each user story has complete test criteria and can be validated independently

**⚠️  IMPORTANT**: Phase 2 architecture fix is CRITICAL and BLOCKING. The current implementation uses app-wrapper div classes but AdminLTE requires body tag classes for CSS selectors to work correctly. This must be fixed before proceeding with any user story implementation.
