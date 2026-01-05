# Tasks: AdminLTE Layout Component Separation

**Feature**: 001-layout-component-split
**Branch**: `001-layout-component-split`
**Date**: January 5, 2026

## Task Summary

**Total Tasks**: 34
**Completed**: 34 (100%)
**User Stories**: 2 (P1: Component Isolation ✅, P2: Composition Flexibility ✅)
**Status**: ✅ **READY FOR MERGE**

---

## Phase 1: Setup

**Goal**: Initialize project structure and verify django-cotton configuration

- [X] T001 Create component directory structure in mvp/templates/cotton/app/
- [X] T002 Verify django-cotton is configured in INSTALLED_APPS and template loaders

---

## Phase 2: Foundational Prerequisites

**Goal**: Establish shared understanding and extract requirements from existing layout

- [X] T003 [P] Document current mvp/base.html template structure and all existing template blocks
- [X] T004 [P] Extract AdminLTE CSS class requirements from existing layout (grid areas, modifiers)
- [X] T005 [P] Create test fixtures for component rendering tests in tests/conftest.py

---

## Phase 3: User Story 1 - Component Isolation (Priority: P1)

**Story Goal**: Split AdminLTE layout into 5 independent Cotton components with full isolation between sections

**Independent Test Criteria**:

- Each component renders independently with valid HTML structure
- mvp/base.html successfully composes all 5 components
- Overriding one component block doesn't affect others
- All existing template blocks remain functional
- Existing example/dashboard.html works without changes

### Component Creation (Flat Files)

- [X] T006 [P] [US1] Create wrapper component in mvp/templates/cotton/app/wrapper.html with c-vars (body_class, fixed_sidebar, sidebar_expand) and named slots (header, sidebar, main, footer)
- [X] T008 [P] [US1] Create footer component in mvp/templates/cotton/app/footer.html with c-vars (text, class) and named slots (right, default)

### Header Sub-Components

- [X] T007 [US1] Create header directory structure mvp/templates/cotton/app/header/
- [X] T033 [P] [US1] Create header/toggle.html component with c-vars for sidebar toggle button
- [X] T034 [US1] Create header/index.html orchestrator with integrated navbar structure (left/right sections) and c-vars (class, container_class)

### Sidebar Sub-Components

- [X] T009 [US1] Create sidebar directory structure mvp/templates/cotton/app/sidebar/
- [X] T010 [P] [US1] Create sidebar/branding.html component with c-vars (brand_text, brand_logo, brand_url)
- [X] T011 [P] [US1] Create sidebar/menu.html component with c-vars (theme, class) and default slot for menu items
- [X] T012 [US1] Create sidebar/index.html orchestrator that composes branding and menu sub-components with sidebar c-vars

### Main Sub-Components

- [X] T013 [US1] Create main directory structure mvp/templates/cotton/app/main/
- [X] T014 [P] [US1] Create main/content_header.html component with c-vars (show_header, container_class) and header slot
- [X] T015 [P] [US1] Create main/content.html component with default slot for main content
- [X] T016 [US1] Create main/index.html orchestrator that composes content_header and content sub-components

### Integration

- [X] T017 [US1] Refactor mvp/templates/mvp/base.html to use new component system while preserving all existing template blocks (page_title, breadcrumbs, sidebar_menu, navbar_left, navbar_right, content, app_header, app_sidebar, app_footer)
- [X] T018 [US1] Verify backward compatibility: existing example/dashboard.html renders without modifications

### Testing

**Note**: Unit tests should include edge case validation: invalid c-var values, missing c-var defaults, and empty slots (per spec.md Edge Cases section).

- [X] T019 [P] [US1] Create tests/test_app_components.py with unit tests for wrapper component (3 c-var configurations, slot rendering)
- [X] T020 [P] [US1] Add unit tests for header/toggle.html component (toggle button rendering, c-vars)
- [X] T021 [P] [US1] Add unit tests for header/index.html component (navbar structure, left/right slots, sub-component composition)
- [X] T022 [P] [US1] Add unit tests for footer component (text override, right slot, default slot)
- [X] T023 [P] [US1] Add unit tests for sidebar/branding.html (logo presence/absence, brand_url)
- [X] T024 [P] [US1] Add unit tests for sidebar/menu.html (theme application, default slot)
- [X] T025 [P] [US1] Add unit tests for sidebar/index.html (sub-component composition)
- [X] T026 [P] [US1] Add unit tests for main/content_header.html (show_header toggle, header slot)
- [X] T027 [P] [US1] Add unit tests for main/content.html (default slot rendering)
- [X] T028 [P] [US1] Add unit tests for main/index.html (sub-component composition)
- [X] T029 [US1] Create tests/test_base_template_integration.py with integration tests for full mvp/base.html layout composition with all components

---

## Phase 4: User Story 2 - Composition Flexibility (Priority: P2)

**Story Goal**: Validate that components can be composed flexibly for different layouts

**Independent Test Criteria**:

- Custom template with subset of components renders correctly
- Components respect individual c-var configurations without interference
- Missing optional components don't cause errors
- Existing example/dashboard.html demonstrates full composition

**Status**: ✅ **COMPLETE** - No additional implementation required. User Story 2 acceptance scenarios can be validated using the existing example/dashboard.html template, which demonstrates flexible composition of all 5 components with various configurations. Per clarification session, no additional example templates or views are needed.

---

## Phase 5: Polish & Production Ready

**Goal**: Documentation, edge case handling, and final validation

- [X] T030 [P] Update quickstart.md to reference actual component file paths and verify all code examples are correct
- [X] T031 [P] Run full test suite and verify all 45+ tests pass (poetry run pytest)
- [X] T032 Run linting and formatting checks (poetry run ruff check .; poetry run djlint mvp/templates)
- [X] T035 Verify browser rendering: Load example/dashboard.html and inspect that all layout sections render with correct AdminLTE structure

---

## Dependencies & Execution Order

### Critical Path (Must Complete in Order)

1. **Phase 1 (Setup)** → T001, T002
2. **Phase 2 (Foundation)** → T003, T004, T005 (can run in parallel after Phase 1)
3. **Phase 3 (US1 Implementation)** → Must complete in sequence:
   - Create component directories → Create components → Integration → Testing
4. **Phase 5 (Polish)** → After Phase 3 complete

### Parallel Execution Opportunities

**After T005 (Foundation Complete)**:

- Parallel Group A: T006, T007, T008 (flat file components)
- Parallel Group B: T010, T011 (sidebar sub-components, after T009)
- Parallel Group C: T014, T015 (main sub-components, after T013)

**After T018 (Integration Complete)**:

- Parallel Group D: T019-T028 (all test files can be created in parallel)

---

## Implementation Strategy

### MVP Delivery (Phase 3 Only)

**Deliverables**:

- 11 component template files (2 flat + 9 in subdirectories)
- 1 refactored mvp/base.html
- 2 test files with 45+ tests
- Backward compatible with existing templates

**Validation**:

- All tests pass
- example/dashboard.html works without changes
- Each component independently testable
- Full layout composition validated

### Incremental Approach

1. **Sprint 1**: Phases 1-2 (Setup + Foundation) - ~2 hours
2. **Sprint 2**: Phase 3 Components (T006-T016) - ~6 hours
3. **Sprint 3**: Phase 3 Integration (T017-T018) - ~2 hours
4. **Sprint 4**: Phase 3 Testing (T019-T028) - ~4 hours
5. **Sprint 5**: Phase 5 Polish (T029-T032) - ~2 hours

**Total Estimated Effort**: 16 hours

---

## Success Criteria Mapping

| Success Criterion | Tasks | Validation |
|-------------------|-------|------------|
| **SC-001**: 100% isolation between layout sections | T006-T016, T017 | T019-T028 (unit tests verify independent rendering) |
| **SC-002**: 0% feature loss from AdminLTE | T004, T006-T016 | T028 (integration tests verify full layout structure) |
| **SC-003**: All 5 sections independently testable | T019-T028 | Each component has 3-5 test cases with various configurations |
| **SC-004**: <10 declarations for custom layouts | T017, T018 | example/dashboard.html demonstrates composition |
| **SC-005**: 50% file size reduction | T006-T016 | Compare line counts: monolithic base.html vs individual components |

---

## Testing Matrix

| Component | Test File | Test Cases | Coverage |
|-----------|-----------|------------|----------|
| wrapper.html | test_app_components.py | 3-5 tests | c-vars, slots, CSS classes |
| header/toggle.html | test_app_components.py | 2-3 tests | toggle button, c-vars |
| header/index.html | test_app_components.py | 3-5 tests | navbar structure, slots, composition |
| footer.html | test_app_components.py | 3-5 tests | text override, slots |
| sidebar/branding.html | test_app_components.py | 3-5 tests | logo, brand text, URL |
| sidebar/menu.html | test_app_components.py | 3-5 tests | theme, CSS class, slot |
| sidebar/index.html | test_app_components.py | 3-5 tests | sub-component composition |
| main/content_header.html | test_app_components.py | 3-5 tests | show_header toggle, slot |
| main/content.html | test_app_components.py | 3-5 tests | default slot rendering |
| main/index.html | test_app_components.py | 3-5 tests | sub-component composition |
| mvp/base.html | test_base_template_integration.py | 5-10 tests | full layout composition, backward compatibility |

**Total Test Coverage**: ~45-55 tests across 11 components + integration

---

## Notes

### Snake_Case Naming Convention (CRITICAL)

All component files MUST use snake_case following django-cotton conventions:

- ✅ `content_header.html`
- ❌ `content-header.html` (kebab-case is NOT django-cotton convention)

### Backward Compatibility

All existing template blocks in mvp/base.html MUST be preserved:

- `page_title`, `breadcrumbs`, `sidebar_menu`
- `navbar_left`, `navbar_right`
- `content`
- `app_header`, `app_sidebar`, `app_footer`

### Test-First Approach

Per Constitution Principle I (Test-First):

- Write tests first (Red)
- Implement component (Green)
- Refactor if needed
- This is enforced in task ordering: Testing tasks follow implementation tasks

### No Browser Testing

Per clarification: pytest-playwright coverage is deferred. This feature maintains existing scope (no browser tests in current implementation). All testing via `render_to_string`.
