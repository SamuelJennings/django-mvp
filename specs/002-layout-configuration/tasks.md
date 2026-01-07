# Tasks: AdminLTE Layout Configuration System

**Input**: Design documents from `/specs/002-layout-configuration/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Updated**: 2026-01-07

**Tests**: Tests are REQUIRED for behavior changes. Use pytest + pytest-django for backend/integration.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Task Summary

**Status**: Core component implementation ALREADY COMPLETE (per research.md).
**Remaining Work**: Documentation, testing verification, and unified demo page implementation.

- **Foundational**: ✅ Complete (component exists at `mvp/templates/cotton/app/index.html`)
- **User Story 1** (Apply Basic Layout Variations - P1): 10 tasks
- **User Story 2** (Combine Multiple Fixed Elements - P2): 6 tasks
- **User Story 3** (Configure Layout Per-Page - P3): 6 tasks
- **User Story 4** (Interactive Layout Demo Page - P2): 16 tasks
- **Polish & Cross-Cutting**: 8 tasks
- **Total**: 46 tasks

---

## Phase 1: Foundational (ALREADY COMPLETE per research.md)

**Status**: ✅ The `<c-app>` component already implements all layout attributes

**Evidence** (from research.md):

- Location: `mvp/templates/cotton/app/index.html`
- Implements: `fixed_sidebar`, `fixed_header`, `fixed_footer`, `sidebar_expand`
- CSS classes: `.layout-fixed`, `.fixed-header`, `.fixed-footer`, `.sidebar-expand-{breakpoint}`

**Action**: No implementation work needed for core component - proceed directly to documentation and demo page

---

## Phase 2: User Story 1 - Apply Basic Layout Variations (Priority: P1) 🎯 MVP

**Goal**: Document and test existing layout attribute functionality so developers can use fixed sidebar, header, or footer

**Independent Test**: Verify component renders correct CSS classes for each fixed attribute

### Tests for User Story 1 (REQUIRED)

> **NOTE: Write these tests FIRST, observe existing implementation PASSES**

- [ ] T001 [P] [US1] Test fixed_sidebar renders `.layout-fixed` class in `tests/test_app_layout.py`
- [ ] T002 [P] [US1] Test fixed_header renders `.fixed-header` class in `tests/test_app_layout.py`
- [ ] T003 [P] [US1] Test fixed_footer renders `.fixed-footer` class in `tests/test_app_layout.py`
- [ ] T004 [P] [US1] Test default (no attributes) renders no fixed classes in `tests/test_app_layout.py`
- [ ] T005 [P] [US1] Test sidebar_expand renders `.sidebar-expand-{value}` class in `tests/test_app_layout.py`

### Documentation for User Story 1

- [ ] T006 [P] [US1] Document `fixed_sidebar` attribute in `docs/components/app.md`
- [ ] T007 [P] [US1] Document `fixed_header` attribute in `docs/components/app.md`
- [ ] T008 [P] [US1] Document `fixed_footer` attribute in `docs/components/app.md`
- [ ] T009 [P] [US1] Document `sidebar_expand` attribute and breakpoints in `docs/components/app.md`
- [ ] T010 [P] [US1] Add basic usage examples to `docs/components/app.md`

**Checkpoint**: User Story 1 complete - developers can configure basic fixed layouts

---

## Phase 3: User Story 2 - Combine Multiple Fixed Elements (Priority: P2)

**Goal**: Document and test combinations of fixed attributes (e.g., fixed sidebar + header)

**Independent Test**: Verify multiple fixed attributes work together correctly

### Tests for User Story 2 (REQUIRED)

- [ ] T011 [P] [US2] Test fixed_sidebar + fixed_header combination in `tests/test_app_layout.py`
- [ ] T012 [P] [US2] Test fixed_header + fixed_footer combination in `tests/test_app_layout.py`
- [ ] T013 [P] [US2] Test fixed complete (all three) combination in `tests/test_app_layout.py`
- [ ] T014 [P] [US2] Test fixed attributes with custom sidebar_expand in `tests/test_app_layout.py`

### Documentation for User Story 2

- [ ] T015 [US2] Document attribute combinations in `docs/components/app.md`
- [ ] T016 [US2] Add "Fixed Complete" layout example in `docs/components/app.md`

**Checkpoint**: User Story 2 complete - developers can use complex fixed layouts

---

## Phase 4: User Story 3 - Configure Layout Per-Page or Globally (Priority: P3)

**Goal**: Document template inheritance patterns for global vs per-page layouts

**Independent Test**: Verify layout can be set in base template and overridden in child templates

### Tests for User Story 3 (REQUIRED)

- [ ] T017 [P] [US3] Test base template with fixed layout renders correctly in `tests/test_app_layout.py`
- [ ] T018 [P] [US3] Test child template inheriting layout from base in `tests/test_app_layout.py`
- [ ] T019 [P] [US3] Test child template overriding base layout in `tests/test_app_layout.py`

### Documentation for User Story 3

- [ ] T020 [US3] Document global layout pattern (base template) in `docs/components/app.md`
- [ ] T021 [US3] Document per-page override pattern in `docs/components/app.md`
- [ ] T022 [US3] Add template inheritance examples in `docs/components/app.md`

**Checkpoint**: User Story 3 complete - developers can configure layouts globally or per-page

---

## Phase 5: User Story 4 - Interactive Layout Demo Page (Priority: P2)

**Goal**: Create single unified demo page at `/layout/` for testing all layout configurations interactively

**Independent Test**: Navigate to /layout/, toggle options via form, verify layout updates with query parameters

### Tests for User Story 4 (REQUIRED)

> **NOTE: Write these tests FIRST**

- [X] T023 [P] [US4] Test `/layout/` view renders with default state (no query params) in `tests/test_unified_layout_demo.py`
- [X] T024 [P] [US4] Test `/layout/?fixed_sidebar=on` applies fixed sidebar in `tests/test_unified_layout_demo.py`
- [X] T025 [P] [US4] Test `/layout/?fixed_header=on&fixed_footer=on` applies both in `tests/test_unified_layout_demo.py`
- [X] T026 [P] [US4] Test `/layout/?fixed_sidebar=on&fixed_header=on&fixed_footer=on` applies all three in `tests/test_unified_layout_demo.py`
- [X] T027 [P] [US4] Test `/layout/?breakpoint=md` applies correct breakpoint in `tests/test_unified_layout_demo.py`
- [X] T028 [P] [US4] Test invalid breakpoint falls back to default "lg" in `tests/test_unified_layout_demo.py`
- [X] T029 [P] [US4] Test form checkboxes reflect current query param state in `tests/test_unified_layout_demo.py`
- [X] T030 [P] [US4] Test dropdown reflects current breakpoint in `tests/test_unified_layout_demo.py`

### Implementation for User Story 4

- [X] T031 [US4] Create `layout_demo` view function in `example/views.py`
  - Parse query parameters: `fixed_sidebar`, `fixed_header`, `fixed_footer`, `breakpoint`
  - Validate breakpoint against ['sm', 'md', 'lg', 'xl', 'xxl']
  - Render `example/layout_demo.html` with context
- [X] T032 [US4] Add URL route for `/layout/` in `example/urls.py`
  - Pattern: `path('layout/', views.layout_demo, name='layout_demo')`
- [X] T033 [US4] Create `example/templates/example/layout_demo.html` template with split layout:
  - Extend base with `<c-app>` using context variables for attributes
  - Use Bootstrap grid: `.row` with `.col-lg-8` (main) and `.col-lg-4` (sidebar)
- [X] T034 [US4] Implement main content area (left side, col-lg-8) in layout_demo.html:
  - Card with header "Layout Configuration Demo"
  - Helper text: "Scroll to test fixed element behavior"
  - Long-form content: multiple sections with headings, paragraphs, lists, tables
  - Total 2-3 viewport heights of scrollable content
- [X] T035 [US4] Implement configuration sidebar (right side, col-lg-4) in layout_demo.html:
  - Card with sticky positioning (`position-sticky, top: 1rem`)
  - Header: "Configuration"
  - Form with GET method, action=`{% url 'layout_demo' %}`
  - Three checkboxes: fixed_sidebar, fixed_header, fixed_footer (checked based on context)
  - Dropdown: breakpoint selector with options sm/md/lg/xl/xxl (selected based on context)
  - Submit button: "Apply Configuration"
  - Visual indicators section showing:
    - Current body classes (e.g., `layout-fixed fixed-header`)
    - Active configuration state (which options are enabled)
- [X] T036 [US4] Add "Layout Demo" menu item in `example/menus.py`
  - Position: Immediately below Dashboard link (after id="dashboard")
  - Label: "Layout Demo"
  - URL: `/layout/` or `{% url 'layout_demo' %}`
  - Icon: "settings" or "tune" (use django-easy-icons if available)
- [X] T037 [US4] Verify sidebar has 12-15 dummy menu items for scrolling test
  - Check existing `example/menus.py` menu definition
  - Add additional dummy items if needed to demonstrate sidebar scrolling
- [X] T038 [US4] Add helper text to demo page explaining:
  - "Use checkboxes to toggle fixed properties"
  - "Use dropdown to test responsive breakpoints"
  - "Scroll page to see fixed elements stay in place"
  - "Resize browser window to test breakpoint transitions"

**Checkpoint**: User Story 4 complete - interactive demo page functional at `/layout/`

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

### Edge Case Testing

- [ ] T039 [P] Test custom class attribute doesn't conflict with fixed classes in `tests/test_app_layout.py`
- [ ] T040 [P] Test all breakpoint values (sm, md, lg, xl, xxl) render correctly in `tests/test_app_layout.py`

### Documentation & Validation

- [ ] T041 Verify all examples in `docs/components/app.md` are accurate and working
- [ ] T042 Add troubleshooting section to `docs/components/app.md`
- [X] T043 Update CHANGELOG.md with feature additions
- [ ] T044 Update README.md with layout configuration quickstart

### Quality Gates

- [X] T045 Run `poetry run pytest` - all tests must pass
- [X] T046 Run `poetry run ruff check .` - all linting must pass (for new code)
- [X] T047 Run `poetry run ruff format .` - apply formatting (for new code)
- [ ] T048 Run djlint on template files in mvp/templates/ and example/templates/

### Manual Validation

- [ ] T049 Manual test: Verify `/layout/` demo page in browser
- [ ] T050 Manual test: Toggle all checkbox combinations and verify layout updates
- [ ] T051 Manual test: Test all breakpoint values via dropdown
- [ ] T052 Manual test: Verify responsive breakpoints at different viewport sizes
- [ ] T053 Manual test: Test in Chrome, Firefox, Safari, Edge (per SC-002)
- [ ] T054 Manual test: Verify scrolling behavior with long content (per SC-003)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: ✅ ALREADY COMPLETE - no work needed
- **User Story 1 (Phase 2)**: Can start immediately (no dependencies)
- **User Story 2 (Phase 3)**: Can start immediately (independent of US1)
- **User Story 3 (Phase 4)**: Can start immediately (independent)
- **User Story 4 (Phase 5)**: Can start immediately (independent demo page)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - documents existing core functionality
- **User Story 2 (P2)**: No blocking dependencies
- **User Story 3 (P3)**: No blocking dependencies
- **User Story 4 (P2)**: No blocking dependencies

### Within Each User Story

**User Stories 1-3** (Tests + Documentation):

- Tests can all run in parallel (T001-T005, T011-T014, T017-T019)
- Documentation tasks can run in parallel after tests
- Tests should be run first to verify existing implementation

**User Story 4** (Demo Page):

- All tests (T023-T030) can run in parallel
- View (T031) must be done before URL (T032)
- Template structure (T033) before content implementation (T034-T035)
- Menu item (T036) can be done in parallel with template work
- Sidebar items check (T037) can be done in parallel
- Helper text (T038) can be added while working on template

### Parallel Opportunities

- All test creation tasks marked [P] within a story can run in parallel
- All documentation tasks marked [P] can run in parallel
- User Stories 1, 2, 3, and 4 can ALL be worked on in parallel by different team members
- All Polish tasks can run in parallel

---

## Parallel Team Strategy

With 4 developers working in parallel:

```bash
# All phases can start immediately since Phase 1 is complete

Developer A: User Story 1 (P1 - Highest Priority)
- T001-T005: Write and run tests (parallel batch)
- T006-T010: Write documentation (parallel batch)

Developer B: User Story 2 (P2)
- T011-T014: Write and run tests (parallel batch)
- T015-T016: Write documentation

Developer C: User Story 3 (P3)
- T017-T019: Write and run tests (parallel batch)
- T020-T022: Write documentation

Developer D: User Story 4 (P2)
- T023-T030: Write all tests (parallel batch)
- T031-T038: Implement demo page (with some parallelism)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. ✅ Phase 1 already complete (core implementation exists)
2. Complete Phase 2: User Story 1 (tests + docs for basic fixed layouts)
3. **STOP and VALIDATE**: Run tests, verify docs are clear
4. Deploy/demo - developers can now use fixed layouts!

### Incremental Delivery

1. Add User Story 2 (combinations) → Test → Deploy
2. Add User Story 3 (template patterns) → Test → Deploy
3. Add User Story 4 (interactive demo) → Test → Deploy
4. Polish phase → Final validation → Release
5. Each story adds value without breaking previous stories

### Time Estimates

- **User Story 1**: 2-3 hours (5 tests + 5 doc sections)
- **User Story 2**: 1-2 hours (4 tests + 2 doc sections)
- **User Story 3**: 1-2 hours (3 tests + 3 doc sections)
- **User Story 4**: 4-6 hours (8 tests + view + template + menu + content)
- **Polish**: 2-3 hours (edge cases + validation + quality gates)
- **Total**: 10-16 hours

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Core `<c-app>` component implementation is ALREADY COMPLETE (per research.md)
- Focus is on documentation, testing verification, and unified demo page
- Demo page replaces two separate demo views from old plan with single `/layout/` endpoint
- Each user story is independently completable and testable
- Verify existing component works before adding docs/tests
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

---

## Success Criteria (from spec.md)

- ✅ **SC-001**: Developers can configure layout in under 2 minutes (component ready)
- **SC-002**: Layout renders correctly in all modern browsers (validate in T053)
- **SC-003**: Fixed elements work with 10,000+ lines (validate in T054)
- **SC-004**: Documentation with examples (complete in T006-T022)
- **SC-005**: <50ms page load impact (inherent - no JS overhead)
